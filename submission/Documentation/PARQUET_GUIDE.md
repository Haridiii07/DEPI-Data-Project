# Parquet Guide

This document explains why the Student Performance Dashboard adopts Apache Parquet, how to work with it, and how it coexists with the legacy CSV workflow.

---

## 1. Why Parquet?

### Storage Benefits
- ~95% compression: `cleaned_students.csv` (1.6 GB) → `cleaned_students.parquet` (~75 MB)
- Columnar layout lets you read only the columns you need
- Schema + data types embedded in the file

### Performance Benefits
- 10–50× faster read times for analytics workloads
- Less memory pressure because columns stream lazily
- Works natively with DuckDB and pandas

```python
import pandas as pd

# CSV: loads everything into memory
df = pd.read_csv('data/processed/milestone1_real/cleaned_students.csv')  # ~30 seconds

# Parquet: pull only required columns
scores = pd.read_parquet(
    'data/processed/milestone1_real/cleaned_students.parquet',
    columns=['score']
)  # ~2 seconds
```

---

## 2. Conversion Workflow

1. Ensure cleaned CSV batches exist (either downloaded or regenerated).
2. Run:

```bash
python src/etl/convert_to_parquet.py
```

3. Script behavior:
   - Scans `data/processed/milestone1_real/students_batch_XX_100K_cleaned.csv`
   - Produces `.parquet` siblings with identical names
   - Keeps CSV source files untouched for backward compatibility

---

## 3. Assembly Workflow

`src/etl/assemble_dataset.py` concatenates the Parquet batches into a single file (`cleaned_students.parquet`). Highlights:

- Auto-discovers `students_batch_01` … `students_batch_10`
- Supports deterministic sampling (`--create-sample --rows-per-batch 10000`)
- Preserves original CSV logic in comments for historical reference

---

## 4. Compatibility Notes

| Scenario | Recommendation |
|----------|----------------|
| Legacy scripts expect CSV | Use the original `cleaned_students.csv` workflow (see commented code in `assemble_dataset.py`). |
| Need zipped artifacts | Zip CSV outputs; Parquet already compresses efficiently. |
| Cloud storage upload | Prefer Parquet; it reduces transfer time dramatically. |
| Cross-platform paths | Use forward slashes (`data/milestone1_real/...`). |

---

## 5. DuckDB Integration

DuckDB can read Parquet files without importing:

```sql
SELECT *
FROM 'data/processed/milestone1_real/cleaned_students.parquet'
LIMIT 10;
```

Within the Milestone 2 notebook:
- Parquet files are registered as external tables
- ETL pipeline builds star schema tables directly from Parquet

---

## 6. Tips & Best Practices

- Keep Parquet files under version control only for samples (`sample_100K_students.parquet`); large artifacts should stay in data storage.
- When debugging schema issues, compare `df.dtypes` between CSV and Parquet to ensure type preservation.
- Use `columns=[...]` when calling `read_parquet` to minimize memory usage.
- Always run commands from the project root so relative paths resolve correctly.

---

## 7. Related Documentation

- Setup steps: `docs/SETUP_GUIDE.md`
- SQL analytics: `docs/SQL_ANALYTICS.md`
- Data dictionary: `docs/data_dictionary.md`


