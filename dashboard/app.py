import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import duckdb
import os

# Page Config
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database Connection
@st.cache_resource
def get_connection():
    # Try to find the database file in likely locations
    possible_paths = [
        "scripts/student_performance.duckdb",
        "../scripts/student_performance.duckdb",
        "data/milestone1_real/student_performance.duckdb",
        "student_performance.duckdb"
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
            
    if not db_path:
        st.error("Database file not found! Please run `scripts/build_database.py` first.")
        return None
        
    conn = duckdb.connect(db_path, read_only=True)
    return conn

conn = get_connection()

# Sidebar Filters
st.sidebar.title("🎓 Filters")

if conn:
    # Cohort (Year) Filter
    years = conn.execute("SELECT DISTINCT year FROM dim_date ORDER BY year DESC").fetchdf()['year'].tolist()
    selected_year = st.sidebar.selectbox("Select Cohort (Year)", ["All"] + years)
    
    # University Type Filter
    uni_types = conn.execute("SELECT DISTINCT university_type FROM dim_university ORDER BY university_type").fetchdf()['university_type'].tolist()
    selected_type = st.sidebar.multiselect("University Type", uni_types, default=uni_types)
    
    # Subject Filter
    subjects = conn.execute("SELECT DISTINCT subject FROM dim_course ORDER BY subject").fetchdf()['subject'].tolist()
    selected_subject = st.sidebar.selectbox("Subject", ["All"] + subjects)

# Main Content
st.title("🎓 Student Performance Analytics")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "👤 Student Profile", "📈 Cohort Analysis"])

if conn:
    # Build Base Query
    base_query = """
        SELECT 
            f.score,
            f.attendance_flag,
            f.grade,
            d.year,
            u.university_name,
            u.university_type,
            c.subject
        FROM fact_student_performance f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_university u ON f.university_key = u.university_key
        JOIN dim_course c ON f.course_key = c.course_key
        WHERE 1=1
    """
    
    params = []
    if selected_year != "All":
        base_query += " AND d.year = ?"
        params.append(selected_year)
    
    if selected_type:
        placeholders = ','.join(['?'] * len(selected_type))
        base_query += f" AND u.university_type IN ({placeholders})"
        params.extend(selected_type)
        
    if selected_subject != "All":
        base_query += " AND c.subject = ?"
        params.append(selected_subject)

    # Load Data
    df = conn.execute(base_query, params).fetchdf()

    # --- TAB 1: OVERVIEW ---
    with tab1:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        avg_score = df['score'].mean()
        attendance_rate = df['attendance_flag'].mean() * 100
        total_students = len(df)
        pass_rate = (len(df[df['score'] >= 60]) / total_students * 100) if total_students > 0 else 0
        
        col1.metric("Avg Score", f"{avg_score:.1f}", delta_color="normal")
        col2.metric("Attendance Rate", f"{attendance_rate:.1f}%", delta_color="normal")
        col3.metric("Total Records", f"{total_students:,}")
        col4.metric("Pass Rate", f"{pass_rate:.1f}%")
        
        st.markdown("---")
        
        # Charts
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Score Distribution")
            fig_hist = px.histogram(df, x="score", nbins=20, title="Score Distribution", color_discrete_sequence=['#3b82f6'])
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with c2:
            st.subheader("Performance by University Type")
            if 'university_type' in df.columns:
                avg_by_type = df.groupby('university_type')['score'].mean().reset_index()
                fig_bar = px.bar(avg_by_type, x='university_type', y='score', title="Average Score by University Type", color='university_type')
                st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: STUDENT PROFILE (Placeholder) ---
    with tab2:
        st.info("Select a specific student ID to view their detailed profile (Feature coming in next update).")
        st.markdown("### Sample Student Data")
        st.dataframe(df.head(10))

    # --- TAB 3: COHORT ANALYSIS (Heatmaps) ---
    with tab3:
        st.subheader("🔥 Attendance Heatmap")
        st.markdown("Attendance rates by University Type and Subject")
        
        # Heatmap Query
        heatmap_query = """
            SELECT 
                u.university_type,
                c.subject,
                AVG(CAST(f.attendance_flag AS INTEGER)) as attendance_rate
            FROM fact_student_performance f
            JOIN dim_university u ON f.university_key = u.university_key
            JOIN dim_course c ON f.course_key = c.course_key
            GROUP BY u.university_type, c.subject
        """
        df_heatmap = conn.execute(heatmap_query).fetchdf()
        
        pivot_df = df_heatmap.pivot(index='university_type', columns='subject', values='attendance_rate')
        
        fig_heat = px.imshow(
            pivot_df,
            labels=dict(x="Subject", y="University Type", color="Attendance Rate"),
            x=pivot_df.columns,
            y=pivot_df.index,
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.subheader("📈 Score Trends")
        # Trend Query
        trend_query = """
            SELECT 
                d.year,
                AVG(f.score) as avg_score
            FROM fact_student_performance f
            JOIN dim_date d ON f.date_id = d.date_id
            GROUP BY d.year
            ORDER BY d.year
        """
        df_trend = conn.execute(trend_query).fetchdf()
        fig_line = px.line(df_trend, x='year', y='avg_score', markers=True, title="Average Score Trend Over Years")
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.warning("Please build the database to view the dashboard.")
