import duckdb
import os
from pathlib import Path
import sys

def convert_to_parquet():
    """
    Converts the raw data into a Star Schema and saves as separate Parquet files.
    This allows for faster loading and cloud deployment without heavy DB files.
    """
    print("🔧 Starting Parquet Conversion Process...")
    
    # Define paths
    base_dir = Path(__file__).parent.parent.parent
    data_path = base_dir / 'data' / 'cleaned_students.parquet'
    output_dir = base_dir / 'data' / 'star_schema'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if data exists, if not, try to stitch it
    if not data_path.exists():
        print(f"⚠️ Data file not found at {data_path}")
        print("🧵 Attempting to stitch file from parts...")
        
        part1 = data_path.parent / f"{data_path.name}.part1"
        if part1.exists():
            with open(data_path, 'wb') as outfile:
                i = 1
                while True:
                    part_path = data_path.parent / f"{data_path.name}.part{i}"
                    if not part_path.exists():
                        break
                    print(f"   - Merging {part_path.name}...")
                    with open(part_path, 'rb') as infile:
                        outfile.write(infile.read())
                    i += 1
            print("✅ File stitched successfully!")
        else:
            print(f"❌ Error: Data parts not found.")
            sys.exit(1)
            
    print(f"📂 Data source: {data_path}")
    print(f"💾 Output directory: {output_dir}")
    
    try:
        # Connect to in-memory DuckDB
        conn = duckdb.connect(database=':memory:')
        
        # 1. Load Raw Data
        print("1️⃣  Loading raw data...")
        conn.execute(f"CREATE OR REPLACE VIEW raw_student_data AS SELECT * FROM '{data_path.as_posix()}'")
        
        # 2. Create Staging Table
        print("2️⃣  Creating staging table...")
        conn.execute("""
            CREATE TABLE staging_student_performance AS
            SELECT 
                CAST(student_id AS VARCHAR) AS student_id,
                CAST(student_name AS VARCHAR) AS student_name,
                CAST(major AS VARCHAR) AS major,
                CAST(university AS VARCHAR) AS university,
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
            WHERE student_id IS NOT NULL AND date IS NOT NULL;
        """)
        
        # 3. Create and Export Dimension Tables
        print("3️⃣  Creating and exporting dimension tables...")
        
        # dim_student
        conn.execute("""
            CREATE TABLE dim_student AS
            SELECT 
                ROW_NUMBER() OVER (ORDER BY student_id) AS student_key,
                student_id,
                student_name,
                major
            FROM (SELECT DISTINCT student_id, student_name, major FROM staging_student_performance);
        """)
        conn.execute(f"COPY dim_student TO '{output_dir / 'dim_student.parquet'}' (FORMAT PARQUET);")
        print("   - dim_student.parquet created")
        
        # dim_university
        conn.execute("""
            CREATE TABLE dim_university AS
            SELECT 
                ROW_NUMBER() OVER (ORDER BY university) AS university_key,
                university AS university_name,
                ipeds_institutional_factor
            FROM (SELECT DISTINCT university, ipeds_institutional_factor FROM staging_student_performance);
        """)
        conn.execute(f"COPY dim_university TO '{output_dir / 'dim_university.parquet'}' (FORMAT PARQUET);")
        print("   - dim_university.parquet created")
        
        # dim_course
        conn.execute("""
            CREATE TABLE dim_course AS
            SELECT 
                ROW_NUMBER() OVER (ORDER BY subject, credits, course_level) AS course_key,
                subject,
                credits,
                course_level
            FROM (SELECT DISTINCT subject, credits, course_level FROM staging_student_performance);
        """)
        conn.execute(f"COPY dim_course TO '{output_dir / 'dim_course.parquet'}' (FORMAT PARQUET);")
        print("   - dim_course.parquet created")
        
        # dim_date
        conn.execute("""
            CREATE TABLE dim_date AS
            SELECT 
                ROW_NUMBER() OVER (ORDER BY date) AS date_id,
                strftime('%Y%m%d', date) AS date_key,
                date AS full_date,
                EXTRACT(YEAR FROM date) AS year,
                CASE WHEN EXTRACT(MONTH FROM date) BETWEEN 1 AND 6 THEN 'Spring' ELSE 'Fall' END AS semester,
                EXTRACT(MONTH FROM date) AS month,
                EXTRACT(DAY FROM date) AS day,
                EXTRACT(DOW FROM date) AS day_of_week
            FROM (SELECT DISTINCT date FROM staging_student_performance WHERE date IS NOT NULL);
        """)
        conn.execute(f"COPY dim_date TO '{output_dir / 'dim_date.parquet'}' (FORMAT PARQUET);")
        print("   - dim_date.parquet created")
        
        # 4. Create and Export Fact Table
        print("4️⃣  Creating and exporting fact table...")
        conn.execute("""
            CREATE TABLE fact_student_performance AS
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
        conn.execute(f"COPY fact_student_performance TO '{output_dir / 'fact_student_performance.parquet'}' (FORMAT PARQUET);")
        print("   - fact_student_performance.parquet created")
        
        print("✅ Conversion completed successfully!")
        conn.close()
        
    except Exception as e:
        print(f"❌ Error converting to parquet: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_to_parquet()
