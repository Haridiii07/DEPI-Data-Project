# Data Dictionary

## Student Performance Dataset

**Dataset Name:** `cleaned_students.parquet`  
**Total Records:** ~10,000,000  
**Time Period:** 2010-2024  
**Description:** Cleaned and standardized student academic performance data from top 50 U.S. universities.

---

## Column Definitions

| Column Name | Data Type | Description | Valid Values/Range | Example |
|-------------|-----------|-------------|-------------------|---------|
| `student_id` | VARCHAR | Unique identifier for each student | Format: `UNI##_STU########` | `UNI01_STU00000123` |
| `student_name` | VARCHAR | Anonymized student name | Format: `Student_#####` | `Student_00001` |
| `university` | VARCHAR | Full university name | 50 U.S. universities | `Harvard University` |
| `state` | VARCHAR | U.S. state where university is located | 50 U.S. states + DC | `Massachusetts` |
| `university_type` | VARCHAR | Classification of university | `Ivy League`, `Public`, `Private` | `Ivy League` |
| `subject` | VARCHAR | Academic subject/course | 31 subjects | `Mathematics` |
| `score` | INTEGER | Numerical grade (0-100 scale) | 0-100 | `85` |
| `grade` | VARCHAR(2) | Letter grade | `A+`, `A`, `A-`, `B+`, `B`, `B-`, `C+`, `C`, `C-`, `D+`, `D`, `F` | `A-` |
| `attendance_flag` | BOOLEAN | Whether student attended | `true` (present), `false` (absent) | `true` |
| `performance_category` | VARCHAR | Performance classification | `Excellent`, `High`, `Medium`, `Low`, `Poor` | `High` |
| `year` | INTEGER | Academic year | 2010-2024 | `2023` |
| `semester` | VARCHAR | Academic term | `Fall`, `Spring`, `Summer` | `Fall` |
| `date` | DATE | Date of record (ISO 8601 format) | YYYY-MM-DD | `2023-09-15` |
| `credits` | INTEGER | Course credit hours | 3, 4 | `3` |
| `course_level` | VARCHAR | Academic level | `Undergraduate`, `Graduate` | `Undergraduate` |
| `batch_number` | INTEGER | Processing batch identifier | 1-10 | `5` |

---

## Performance Category Mapping

| Category | Score Range | Description |
|----------|-------------|-------------|
| **Excellent** | 93-100 | Outstanding performance (A, A+) |
| **High** | 77-92 | Above average performance (A-, B+, B) |
| **Medium** | 67-76 | Average performance (B-, C+, C) |
| **Low** | 60-66 | Below average performance (C-, D+) |
| **Poor** | 0-59 | Failing performance (D, F) |

---

## Data Quality Notes

### Cleaning & Standardization
- **Duplicates:** All duplicate records (same `student_id`, `subject`, `date`) removed
- **Nulls:** Records with null `student_id`, `subject`, or `date` excluded
- **Date Format:** All dates converted to ISO 8601 standard (YYYY-MM-DD)
- **Name Anonymization:** Original names replaced with sequential IDs
- **Performance Standardization:** Categories normalized to 5 standard values

### Data Integrity
- **Score Range:** All scores validated to be within 0-100
- **University Mapping:** All universities verified against IPEDS database
- **State Mapping:** Each university mapped to correct U.S. state
- **Type Classification:** Universities classified by verified type

---

## Database Schema Mapping

When loaded into the star schema database (`student_performance.duckdb`), this data is normalized into:

- **`dim_student`**: Student demographics (`student_key`, `student_id`, `student_name`)
- **`dim_university`**: University details (`university_key`, `university_name`, `state`, `university_type`)
- **`dim_course`**: Course information (`course_key`, `subject`, `credits`, `course_level`)
- **`dim_date`**: Date dimension (`date_id`, `full_date`, `year`, `semester`, `month`)
- **`fact_student_performance`**: Performance facts (`fact_id`, foreign keys, `score`, `grade`, `attendance_flag`, `performance_category`)

---

## Usage Examples

### Load Data (Python)
```python
import pandas as pd

# Load full dataset
df = pd.read_parquet('data/milestone1_real/cleaned_students.parquet')

# Load specific columns
df = pd.read_parquet('data/milestone1_real/cleaned_students.parquet', 
                      columns=['student_id', 'subject', 'score'])
```

### Query Data (DuckDB)
```sql
-- Connect to database
SELECT 
    u.university_name,
    c.subject,
    AVG(f.score) as avg_score
FROM fact_student_performance f
JOIN dim_university u ON f.university_key = u.university_key
JOIN dim_course c ON f.course_key = c.course_key
GROUP BY u.university_name, c.subject
ORDER BY avg_score DESC;
```

---

## Contact & Maintenance

**Last Updated:** November 20, 2025  
**Maintained By:** Group 4 (DEPI Project)  
**Version:** 1.0
