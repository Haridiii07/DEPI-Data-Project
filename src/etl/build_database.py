import duckdb
import os
from pathlib import Path
import sys

def build_database():
    """
    Rebuilds the student_performance.duckdb database from the cleaned Parquet file.
    """
    print("🔧 Starting Database Build Process...")
    
    # Define paths
    base_dir = Path(__file__).parent.parent.parent
    data_path = base_dir / 'data' / 'cleaned_students.parquet'
    db_path = base_dir / 'warehouse' / 'student_performance.duckdb'
    # Ensure the warehouse directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if data exists
    if not data_path.exists():
        print(f"❌ Error: Data file not found at {data_path}")
        print("Please run 'python scripts/assemble_dataset.py' first.")
        sys.exit(1)
        
    # Remove existing database if it exists to start fresh
    if db_path.exists():
        try:
            os.remove(db_path)
            print(f"🗑️  Removed existing database: {db_path}")
        except Exception as e:
            print(f"❌ Error removing existing database: {e}")
            sys.exit(1)
            
    print(f"📂 Data source: {data_path}")
    print(f"💾 Database target: {db_path}")
    
    try:
        # Connect to DuckDB
        conn = duckdb.connect(str(db_path))
        
        # 1. Create View from Parquet
        print("1️⃣  Creating raw data view...")
        conn.execute(f"""
            CREATE OR REPLACE VIEW raw_student_data AS
            SELECT * FROM '{data_path.as_posix()}'
        """)
        
        # 2. Create Staging Table
        print("2️⃣  Creating staging table...")
        conn.execute("""
            CREATE TABLE staging_student_performance AS
            SELECT 
                CAST(student_id AS VARCHAR) AS student_id,
                CAST(student_name AS VARCHAR) AS student_name,
                CAST(major AS VARCHAR) AS major,  -- NEW: Added major
                CAST(university AS VARCHAR) AS university,
                -- Removed state and university_type as they are not in the new data
                CAST(subject AS VARCHAR) AS subject,
                CAST(score AS INTEGER) AS score,
                CAST(grade AS VARCHAR(2)) AS grade,
                CAST(attendance_flag AS BOOLEAN) AS attendance_flag,
                CAST(performance_category AS VARCHAR) AS performance_category,
                CAST(year AS INTEGER) AS year,
                CAST(semester AS VARCHAR) AS semester,
                CAST(date AS DATE) AS date,
                CAST(credits AS INTEGER) AS credits,
                CAST(course_level AS VARCHAR) AS course_level,
                CAST(batch_number AS INTEGER) AS batch_number,
                CAST(ipeds_institutional_factor AS INTEGER) AS ipeds_institutional_factor
            FROM raw_student_data
            WHERE student_id IS NOT NULL
              AND date IS NOT NULL;
        """)
        
        # 3. Create Dimension Tables
        print("3️⃣  Creating dimension tables...")
        
        # dim_student
        conn.execute("""
            CREATE TABLE dim_student (
                student_key INTEGER PRIMARY KEY,
                student_id VARCHAR,              
                student_name VARCHAR,
                major VARCHAR  -- NEW: Added major
            );
            
            INSERT INTO dim_student (student_key, student_id, student_name, major)
            SELECT 
                ROW_NUMBER() OVER (ORDER BY student_id) AS student_key,
                student_id,
                student_name,
                major
            FROM (
                SELECT DISTINCT student_id, student_name, major
                FROM staging_student_performance
            ) AS distinct_students;
        """)
        
        # dim_university
        conn.execute("""
            CREATE TABLE dim_university (
                university_key INTEGER PRIMARY KEY,
                university_name VARCHAR(100),
                ipeds_institutional_factor INTEGER
            );
            
            INSERT INTO dim_university (university_key, university_name, ipeds_institutional_factor)
            SELECT 
                ROW_NUMBER() OVER (ORDER BY university) AS university_key,
                university AS university_name,
                ipeds_institutional_factor
            FROM (
                SELECT DISTINCT university, ipeds_institutional_factor
                FROM staging_student_performance
            ) AS distinct_universities;
        """)
        
        # dim_course
        conn.execute("""
            CREATE TABLE dim_course (
                course_key INTEGER PRIMARY KEY,
                subject VARCHAR(100),
                credits INTEGER,
                course_level VARCHAR(50)
            );
            
            INSERT INTO dim_course (course_key, subject, credits, course_level)
            SELECT 
                ROW_NUMBER() OVER (ORDER BY subject, credits, course_level) AS course_key,
                subject,
                credits,
                course_level
            FROM (
                SELECT DISTINCT subject, credits, course_level
                FROM staging_student_performance
            ) AS distinct_courses;
        """)
        
        # dim_date
        conn.execute("""
            CREATE TABLE dim_date (
                date_id INTEGER PRIMARY KEY,
                date_key VARCHAR UNIQUE,
                full_date DATE,
                year INTEGER,
                semester VARCHAR,
                month INTEGER,
                day INTEGER,
                day_of_week INTEGER
            );
            
            INSERT INTO dim_date (date_id, date_key, full_date, year, semester, month, day, day_of_week)
            SELECT 
                ROW_NUMBER() OVER (ORDER BY date) AS date_id,
                strftime('%Y%m%d', date) AS date_key,
                date AS full_date,
                EXTRACT(YEAR FROM date) AS year,
                CASE 
                    WHEN EXTRACT(MONTH FROM date) BETWEEN 1 AND 6 THEN 'Spring'
                    ELSE 'Fall'
                END AS semester,
                EXTRACT(MONTH FROM date) AS month,
                EXTRACT(DAY FROM date) AS day,
                EXTRACT(DOW FROM date) AS day_of_week
            FROM (
                SELECT DISTINCT date
                FROM staging_student_performance
                WHERE date IS NOT NULL
            ) AS distinct_dates;
        """)
        
        # 4. Create Fact Table
        print("4️⃣  Creating fact table...")
        conn.execute("""
            CREATE TABLE fact_student_performance (
                fact_id INTEGER PRIMARY KEY,
                student_key INTEGER,
                university_key INTEGER,
                course_key INTEGER,
                date_id INTEGER,
                score INTEGER,
                grade VARCHAR(2),
                attendance_flag BOOLEAN,
                performance_category VARCHAR(20),
                FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
                FOREIGN KEY (university_key) REFERENCES dim_university(university_key),
                FOREIGN KEY (course_key) REFERENCES dim_course(course_key),
                FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
            );
            
            INSERT INTO fact_student_performance (
                fact_id, student_key, university_key, course_key, date_id,
                score, grade, attendance_flag, performance_category
            )
            SELECT 
                ROW_NUMBER() OVER (ORDER BY st.student_id, st.date, st.subject) AS fact_id,
                s.student_key,
                u.university_key,
                c.course_key,
                d.date_id,
                st.score,
                st.grade,
                st.attendance_flag,
                st.performance_category
            FROM staging_student_performance st
            JOIN dim_student s ON st.student_id = s.student_id
            JOIN dim_university u ON st.university = u.university_name
            JOIN dim_course c ON st.subject = c.subject AND st.credits = c.credits AND st.course_level = c.course_level
            JOIN dim_date d ON st.date = d.full_date;
        """)
        
        # Validation
        fact_count = conn.execute("SELECT COUNT(*) FROM fact_student_performance").fetchone()[0]
        print(f"✅ Database built successfully!")
        print(f"📊 Total records in fact table: {fact_count:,}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error building database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_database()
