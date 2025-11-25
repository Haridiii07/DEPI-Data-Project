import duckdb

conn = duckdb.connect('warehouse/student_performance.duckdb', read_only=True)

# Check student 11's data
query = """
SELECT d.year, d.semester, c.subject, f.score, f.grade, f.attendance_flag
FROM fact_student_performance f
JOIN dim_student s ON f.student_key = s.student_key
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_course c ON f.course_key = c.course_key
WHERE s.student_id = 'UNI00_STU00000011'
ORDER BY d.year DESC, d.semester
"""

df = conn.execute(query).fetchdf()
print(f"Total records for student 11: {len(df)}\n")
print("First 20 records:")
print(df.head(20))
print("\nUnique subjects:", df['subject'].nunique())
print("\nSubjects:", df['subject'].unique()[:10])
print("\nYear range:", df['year'].min(), "to", df['year'].max())
