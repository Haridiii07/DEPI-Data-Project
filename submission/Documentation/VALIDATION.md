# Validation Guide

Commands and snippets to confirm dataset integrity, schema consistency, and pipeline health.

---

## 1. Row Counts

### PowerShell

```powershell
Get-ChildItem "data/milestone1_real/*_cleaned.csv" |
  ForEach-Object {
    "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines)"
  }
```

### Python

```python
import pandas as pd
df = pd.read_csv('data/processed/milestone1_real/cleaned_students.csv')
print('rows:', len(df), 'cols:', df.shape[1])
```

---

## 2. Column Order & Presence

```python
expected = [
    'student_id','student_name','university','state','university_type',
    'subject','score','grade','attendance_flag','performance_category',
    'year','semester','date','credits','course_level','batch_number'
]
df = pd.read_csv('data/processed/milestone1_real/students_batch_01_100K_cleaned.csv', nrows=0)
assert list(df.columns) == expected
```

---

## 3. Distribution Checks

```python
print(df['performance_category'].value_counts())
print(df['attendance_flag'].value_counts())
print(df['state'].value_counts().head(10))
print(pd.to_datetime(df['date'], errors='coerce').notna().mean())
```

Interpretation:
- Performance categories should cover Excellent → Poor
- Attendance flag must be boolean
- States should map to 50 US states + DC
- Date parsing success ratio should be 1.0

---

## 4. Sample Verification

```bash
python src/etl/create_sample_dataset.py
python src/etl/verify_sample.py
```

Expected outputs:
- Deterministic counts per batch (10K rows each when default settings used)
- Summary statistics logged to console

---

## 5. DuckDB Checks

After running `src/etl/build_database.py`, connect via DuckDB CLI or Python:

```sql
SELECT COUNT(*) FROM fact_student_performance;
SELECT COUNT(*) FROM dim_student;
```

Ensure fact-table count matches total input rows (~10M) and dimension counts make sense (e.g., 1M students, 50 universities, 31 subjects).

---

## 6. Dashboard Smoke Test

1. Launch Streamlit (`python -m streamlit run src/dash/app.py`)
2. Confirm the Overview page loads with KPI tiles populated
3. Apply a filter → ensure charts react and no console errors appear

---

## 7. Troubleshooting

If any validation step fails:
- Review scripts/logs for errors
- Refer to `docs/TROUBLESHOOTING.md` for fixes (path issues, missing files, etc.)
- Re-run setup steps from `docs/SETUP_GUIDE.md`

---

## 8. Related Resources

- Data dictionary: `docs/data_dictionary.md`
- SQL details: `docs/SQL_ANALYTICS.md`
- Development practices: `docs/DEVELOPMENT.md`


