import duckdb

conn = duckdb.connect('warehouse/student_performance.duckdb', read_only=True)

# Analyze student patterns
query = """
SELECT 
    s.student_id,
    COUNT(*) as total_courses,
    COUNT(DISTINCT c.subject) as unique_subjects,
    MIN(d.year) as first_year,
    MAX(d.year) as last_year,
    (MAX(d.year) - MIN(d.year) + 1) as year_span
FROM fact_student_performance f
JOIN dim_student s ON f.student_key = s.student_key
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_course c ON f.course_key = c.course_key
GROUP BY s.student_id
ORDER BY total_courses DESC
LIMIT 50
"""

df = conn.execute(query).fetchdf()

print("📊 Student Pattern Analysis (Top 50 by course count)\n")
print(f"Average courses per student: {df['total_courses'].mean():.1f}")
print(f"Average subjects per student: {df['unique_subjects'].mean():.1f}")
print(f"Average year span: {df['year_span'].mean():.1f} years\n")

print("Distribution of courses per student:")
print(df['total_courses'].value_counts().sort_index().head(20))

print(f"\nFirst 10 students:")
print(df[['student_id', 'total_courses', 'unique_subjects', 'first_year', 'last_year', 'year_span']].head(10))

# Check if there are students with very different patterns
print(f"\n🔍 Pattern Check:")
print(f"Students with 1 course: {len(df[df['total_courses'] == 1])}")
print(f"Students with 10+ courses: {len(df[df['total_courses'] >= 10])}")
print(f"Students spanning 10+ years: {len(df[df['year_span'] >= 10])}")
