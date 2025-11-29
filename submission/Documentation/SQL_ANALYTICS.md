# SQL & Analytics Guide

Details for Milestone 2 deliverables: star schema, DuckDB pipeline, key queries, and exported artifacts.

---

## 1. Overview

- **Status:** ✅ Complete
- **Primary file:** `notebooks/Milestone2_3_SQL_and_Visualizations.ipynb`
- **Database:** `warehouse/student_performance.duckdb`
- **Input:** `data/processed/milestone1_real/cleaned_students.parquet`

---

## 2. Star Schema

Dimension tables:
- `dim_student (student_key, student_id, student_name)`
- `dim_university (university_key, university_name, state, university_type)`
- `dim_course (course_key, subject, credits, course_level)`
- `dim_date (date_key, full_date, year, semester, month)`

Fact table:
- `fact_student_performance (fact_key, student_key, university_key, course_key, date_key, score, grade, attendance_flag, performance_category)`

![Entity Relationship Diagram](../assets/ERD%20(Entity%20Relationship%20Diagram)%20based%20on%20the%20database%20design.png)

*The ERD illustrates the central fact table connected to the four dimension tables in a classic star schema to optimize analytical queries.*

---

## 3. ETL Pipeline Steps

1. Load Parquet data directly into DuckDB using `read_parquet`.
2. Create staging views for deduplication and normalization.
3. Materialize dimension tables with surrogate keys.
4. Build the fact table joining dimensions via keys.
5. Run quality checks (row counts, distinct keys).

Typical command (inside the notebook):

```sql
CREATE TABLE dim_student AS
SELECT DISTINCT
  row_number() OVER () AS student_key,
  student_id,
  student_name
FROM parquet_scan('data/processed/milestone1_real/cleaned_students.parquet');
```

---

## 4. Key Analytics & Insights

Queries implemented in the notebook (all exported to CSV under `output/`):

| Analysis | Output | Insight Example |
|----------|--------|-----------------|
| Subject performance | `subject_performance_analysis.csv` | Foreign Language scores average 84.6 |
| Top performers | `top_performers.csv` | Highest-scoring 100 students |
| University type comparison | `performance_by_university_type.csv` | Ivy League maintains highest average |
| Seasonal patterns | `seasonal_performance_patterns.csv` | Spring shows slightly better attendance |
| Attendance vs score | Notebook visualizations | Strong positive correlation |

Visualization types: bar charts, line charts, histograms, attendance heatmaps.

---

## 5. Performance Metrics

- **Data volume:** 10M+ rows in fact table
- **ETL runtime:** <5 seconds on baseline laptop
- **Query latency:** Sub-second for complex aggregations
- **Storage:** DuckDB database ~820 MB

---

## 6. Running the Notebook

```bash
jupyter notebook "notebooks/Milestone2_3_SQL_and_Visualizations.ipynb"
```

Ensure:
- `cleaned_students.parquet` exists (see `docs/SETUP_GUIDE.md`)
- Dependencies installed via `requirements.txt`
- For PowerShell paths, use quotes: `"notebooks\Milestone2_3_SQL_and_Visualizations.ipynb"`

---

## 7. Related Docs

- Dashboard instructions: `docs/DASHBOARD_GUIDE.md`
- Validation checks: `docs/VALIDATION.md`
- Development workflow: `docs/DEVELOPMENT.md`


