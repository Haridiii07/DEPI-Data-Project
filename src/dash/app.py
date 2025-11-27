import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import os
import subprocess
import sys
from pathlib import Path

# Page Config
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 4px;
        color: #4b5563;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0e7ff;
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_connection():
    """
    Creates an in-memory DuckDB connection and loads the Star Schema from Parquet files.
    This ensures fast startup and low memory usage.
    """
    try:
        # Connect to in-memory DuckDB
        conn = duckdb.connect(database=':memory:')
        
        # Define path to Parquet files
        base_dir = Path(__file__).parent.parent.parent
        parquet_dir = base_dir / 'data' / 'star_schema'
        
        # Check if Parquet files exist
        required_files = ['fact_student_performance.parquet', 'dim_student.parquet', 
                          'dim_university.parquet', 'dim_course.parquet', 'dim_date.parquet']
        
        missing_files = [f for f in required_files if not (parquet_dir / f).exists()]
        needs_regeneration = False
        
        # If files exist, check if they have the student_number column
        if not missing_files:
            try:
                # Try to load and check for student_number
                conn.execute(f"CREATE TEMP VIEW temp_dim_student AS SELECT * FROM '{parquet_dir / 'dim_student.parquet'}'")
                test_result = conn.execute("SELECT student_number FROM temp_dim_student LIMIT 1").fetchone()
                conn.execute("DROP VIEW temp_dim_student")
            except Exception:
                # Column doesn't exist, need to regenerate
                st.warning("🔄 Old schema detected. Regenerating with updated structure...")
                import shutil
                if parquet_dir.exists():
                    shutil.rmtree(parquet_dir)
                needs_regeneration = True
        
        # Generate star schema if files are missing or need regeneration
        if missing_files or needs_regeneration:
            # Determine which data file to use based on what's available
            sample_50k = base_dir / 'data' / 'sample_50K_students.parquet'
            full_data = base_dir / 'data' / 'cleaned_students.parquet'
            
            if sample_50k.exists():
                data_path = sample_50k
            elif full_data.exists():
                data_path = full_data
            else:
                # Try to stitch from parts (local development)
                part1 = full_data.parent / f"{full_data.name}.part1"
                if part1.exists():
                    data_path = full_data
                else:
                    st.error("❌ No data source found! Please ensure data files are present.")
                    return None
            
            # Run the conversion script (with loading spinner)
            try:
                with st.spinner('Loading dashboard data...'):
                    build_script_path = base_dir / "src" / "etl" / "convert_to_parquet.py"
                    if not build_script_path.exists():
                        st.error(f"Conversion script not found.")
                        return None
                    
                    subprocess.run([sys.executable, str(build_script_path)], check=True, capture_output=True)
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
                return None
        
        # Load Parquet files as Views
        conn.execute(f"CREATE VIEW fact_student_performance AS SELECT * FROM '{parquet_dir / 'fact_student_performance.parquet'}'")
        conn.execute(f"CREATE VIEW dim_student AS SELECT * FROM '{parquet_dir / 'dim_student.parquet'}'")
        conn.execute(f"CREATE VIEW dim_university AS SELECT * FROM '{parquet_dir / 'dim_university.parquet'}'")
        conn.execute(f"CREATE VIEW dim_course AS SELECT * FROM '{parquet_dir / 'dim_course.parquet'}'")
        conn.execute(f"CREATE VIEW dim_date AS SELECT * FROM '{parquet_dir / 'dim_date.parquet'}'")
        
        return conn
        
    except Exception as e:
        st.error(f"❌ Error connecting to database: {e}")
        return None

conn = get_connection()

@st.cache_data
def get_filter_options(_conn, column, table):
    query = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}"
    if column == "year":
        query = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column} DESC"
    return _conn.execute(query).fetchdf()[column].tolist()

# Sidebar
st.sidebar.title("🎓 Filters")

selected_year = "All"
selected_major = "All"
selected_subject = "All"

if conn:
    years = get_filter_options(conn, "year", "dim_date")
    selected_year = st.sidebar.selectbox("Select Cohort (Year)", ["All"] + years)
    
    majors = get_filter_options(conn, "major", "dim_student")
    selected_major = st.sidebar.selectbox("Major", ["All"] + majors)
    
    subjects = get_filter_options(conn, "subject", "dim_course")
    selected_subject = st.sidebar.selectbox("Subject", ["All"] + subjects)

st.title("🎓 Student Performance Analytics")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📚 Subject & Cohort", "🚨 Risk Analysis", "👤 Student Profile"])

if conn:
    where_conditions = ["1=1"]
    params = []
    
    if selected_year != "All":
        where_conditions.append("d.year = ?")
        params.append(selected_year)
    
    if selected_major != "All":
        where_conditions.append("s.major = ?")
        params.append(selected_major)
        
    if selected_subject != "All":
        where_conditions.append("c.subject = ?")
        params.append(selected_subject)
        
    where_clause = " AND ".join(where_conditions)

    with tab1:
        kpi_query = f"""
            SELECT 
                AVG(f.score) as avg_score,
                AVG(CAST(f.attendance_flag AS INTEGER)) * 100 as attendance_rate,
                COUNT(DISTINCT f.student_key) as total_students,
                SUM(CASE WHEN f.score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pass_rate
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            JOIN dim_student s ON f.student_key = s.student_key
            WHERE {where_clause}
        """
        kpi_data = conn.execute(kpi_query, params).fetchone()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Score", f"{kpi_data[0]:.1f}" if kpi_data[0] else "0.0")
        col2.metric("Attendance Rate", f"{kpi_data[1]:.1f}%" if kpi_data[1] else "0.0%")
        col3.metric("Total Students", f"{kpi_data[2]:,}" if kpi_data[2] else "0")
        col4.metric("Pass Rate", f"{kpi_data[3]:.1f}%" if kpi_data[3] else "0.0%")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Score Distribution")
            hist_query = f"""
                SELECT f.score 
                FROM fact_student_performance f
                JOIN dim_date d ON f.date_id = d.date_id
                JOIN dim_university u ON f.university_key = u.university_key
                JOIN dim_course c ON f.course_key = c.course_key
                JOIN dim_student s ON f.student_key = s.student_key
                WHERE {where_clause}
            """
            df_scores = conn.execute(hist_query, params).fetchdf()
            if not df_scores.empty:
                fig_hist = px.histogram(df_scores, x="score", nbins=20, 
                                      color_discrete_sequence=['#3b82f6'])
                fig_hist.update_layout(plot_bgcolor="white")
                st.plotly_chart(fig_hist, width='stretch')
            
        with c2:
            st.subheader("Performance by Major")
            bar_query = f"""
                SELECT s.major, AVG(f.score) as avg_score
                FROM fact_student_performance f
                JOIN dim_date d ON f.date_id = d.date_id
                JOIN dim_university u ON f.university_key = u.university_key
                JOIN dim_course c ON f.course_key = c.course_key
                JOIN dim_student s ON f.student_key = s.student_key
                WHERE {where_clause}
                GROUP BY s.major
                ORDER BY avg_score DESC
                LIMIT 10
            """
            df_bar = conn.execute(bar_query, params).fetchdf()
            if not df_bar.empty:
                fig_bar = px.bar(df_bar, x='major', y='avg_score', color='major',
                               title="Top Majors by Average Score",
                               color_discrete_sequence=px.colors.qualitative.Prism)
                fig_bar.update_layout(plot_bgcolor="white", showlegend=False)
                st.plotly_chart(fig_bar, width='stretch')

    with tab2:
        st.subheader("📚 Subject Deep Dive")
        
        subject_query = f"""
            SELECT c.subject, AVG(f.score) as avg_score, COUNT(*) as students
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            JOIN dim_student s ON f.student_key = s.student_key
            WHERE {where_clause}
            GROUP BY c.subject
            ORDER BY avg_score DESC
            LIMIT 10
        """
        df_subject = conn.execute(subject_query, params).fetchdf()
        
        if not df_subject.empty:
            fig_sub = px.bar(df_subject, x='avg_score', y='subject', orientation='h',
                           title="Top 10 Subjects by Average Score",
                           color='avg_score', color_continuous_scale='Viridis')
            fig_sub.update_layout(plot_bgcolor="white", yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_sub, width='stretch')
        
        st.markdown("---")
        st.subheader("🔥 Attendance Heatmap")
        
        heatmap_query = f"""
            SELECT 
                s.major,
                c.subject,
                AVG(CAST(f.attendance_flag AS INTEGER)) as attendance_rate
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            JOIN dim_student s ON f.student_key = s.student_key
            WHERE {where_clause}
            GROUP BY s.major, c.subject
        """
        df_heatmap = conn.execute(heatmap_query, params).fetchdf()
        
        if not df_heatmap.empty:
            pivot_df = df_heatmap.pivot(index='major', columns='subject', values='attendance_rate')
            fig_heat = px.imshow(
                pivot_df,
                labels=dict(x="Subject", y="Major", color="Attendance Rate"),
                x=pivot_df.columns,
                y=pivot_df.index,
                color_continuous_scale="RdBu",
                aspect="auto"
            )
            st.plotly_chart(fig_heat, width='stretch')

    with tab3:
        st.subheader("🚨 At-Risk Student Analysis")
        
        risk_count_query = f"""
            SELECT COUNT(*) 
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            JOIN dim_student s ON f.student_key = s.student_key
            WHERE {where_clause} AND (f.score < 60 OR f.attendance_flag = FALSE)
        """
        risk_count = conn.execute(risk_count_query, params).fetchone()[0]
        
        st.metric("⚠️ At-Risk Records", f"{risk_count:,}")
        
        risk_scatter_query = f"""
            SELECT f.score, CAST(f.attendance_flag AS INTEGER) as attendance
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            JOIN dim_student s ON f.student_key = s.student_key
            WHERE {where_clause}
            LIMIT 2000
        """
        df_risk = conn.execute(risk_scatter_query, params).fetchdf()
        
        if not df_risk.empty:
            fig_risk = px.scatter(df_risk, x='attendance', y='score', trendline="ols")
            fig_risk.add_hrect(y0=0, y1=60, line_width=0, fillcolor="red", opacity=0.1)
            st.plotly_chart(fig_risk, width='stretch')
            
        st.subheader("📥 Download At-Risk List")
        risk_list_query = f"""
            SELECT s.student_id, s.student_name, u.university_name, c.subject, f.score
            FROM fact_student_performance f
            JOIN dim_student s ON f.student_key = s.student_key
            JOIN dim_date d ON f.date_id = d.date_id
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            WHERE {where_clause} AND (f.score < 60 OR f.attendance_flag = FALSE)
            LIMIT 1000
        """
        df_risk_list = conn.execute(risk_list_query, params).fetchdf()
        
        if not df_risk_list.empty:
            st.dataframe(df_risk_list)
            st.download_button(
                label="Download At-Risk Data (CSV)",
                data=df_risk_list.to_csv(index=False).encode('utf-8'),
                file_name='at_risk_students.csv',
                mime='text/csv',
            )


    with tab4:
        st.subheader("👤 Student Lookup")
        col_search, col_info = st.columns([1, 2])
        
        with col_search:
            student_number = st.number_input("Enter Student Number (1-10,000)", 
                                            min_value=1, 
                                            max_value=10000, 
                                            step=1,
                                            value=None)
        
        if student_number:
            # Query student by student_number field
            student_query = "SELECT * FROM dim_student WHERE student_number = ?"
            student_info = conn.execute(student_query, [student_number]).fetchdf()
            
            if not student_info.empty:
                with col_info:
                    st.success(f"**Student #{student_number}:** {student_info['student_name'].iloc[0]} | **Major:** {student_info['major'].iloc[0]}")
                
                student_id = student_info['student_id'].iloc[0]
                
                history_query = """
                    SELECT 
                        d.year, d.semester, c.subject, f.score, f.grade, f.attendance_flag
                    FROM fact_student_performance f
                    JOIN dim_student s ON f.student_key = s.student_key
                    JOIN dim_date d ON f.date_id = d.date_id
                    JOIN dim_course c ON f.course_key = c.course_key
                    WHERE s.student_id = ?
                    ORDER BY d.year DESC, d.semester
                """
                history_df = conn.execute(history_query, [student_id]).fetchdf()
                
                if not history_df.empty:
                    st.info(f"📊 **Academic Summary:** {len(history_df)} courses · {history_df['subject'].nunique()} subjects · {history_df['year'].min()}-{history_df['year'].max()}")
                    
                    sum_col1, sum_col2, sum_col3 = st.columns(3)
                    sum_col1.metric("Avg Score", f"{history_df['score'].mean():.1f}")
                    sum_col2.metric("Attendance", f"{history_df['attendance_flag'].mean()*100:.1f}%")
                    sum_col3.metric("Total Courses", len(history_df))
                    
                    st.subheader("📚 Course History")
                    st.markdown("*Each row represents one course taken by this student.*")
                    st.dataframe(history_df, width='stretch')
                else:
                    st.warning("No course history found for this student.")
            else:
                st.warning("Student number not found.")
        else:
            st.info("Enter a student number (1-10,000) to view their academic profile.")

else:
    st.warning("⚠️ Please build the database to view the dashboard.")
