# Troubleshooting Guide

Common issues and fixes for the Student Performance Dashboard project.

---

## 1. Missing Files or Paths

- **Symptom:** `FileNotFoundError: data/milestone1_real/...`
- **Fix:** Run commands from the project root. Verify the data folder contains Parquet batches. Re-run `src/etl/convert_to_parquet.py` and `src/etl/assemble_dataset.py` if necessary.

---

## 2. Module Import Errors

- **Symptom:** `ModuleNotFoundError` when running scripts
- **Fix:** Install requirements (`pip install -r requirements.txt`). Alternatively run `python -m pip install -r requirements.txt` to ensure correct interpreter.

---

## 3. Streamlit Dashboard Won’t Load

- Ensure DuckDB file exists (`warehouse/student_performance.duckdb`). If not, run `python src/etl/build_database.py`.
- Use `python -m streamlit run src/dash/app.py` from repo root.
- If port 8501 is busy, append `--server.port 8502`.

---

## 4. Jupyter Notebook Crashes

- Close other memory-heavy apps; the full dataset requires ~8 GB RAM.
- Use the Parquet sample (`sample_100K_students.parquet`) for lighter runs.
- Restart kernel & run cells sequentially to clear stale state.

---

## 5. PowerShell vs Bash Paths

- Windows PowerShell accepts forward slashes (recommended): `python src/etl/assemble_dataset.py`
- Some commands require quoting: `jupyter notebook "notebooks\Milestone2_3_SQL_and_Visualizations.ipynb"`

---

## 6. Sample Compression

PowerShell command to zip the sample CSV:

```powershell
Compress-Archive -Path data/processed/milestone1_real/sample_100K_students.csv `
  -DestinationPath data/processed/milestone1_real/sample_100K_students.zip -Force
```

---

## 7. Validation Failures

- Re-run checks from `docs/VALIDATION.md`
- Ensure expected columns exist; if not, rerun `clean_students_batches.py`
- Confirm dataset sizes match documentation (1M unique students, 10M+ records)

---

## 8. Performance Issues

- Prefer Parquet when loading data (see `docs/PARQUET_GUIDE.md`)
- Use `columns=[...]` when reading Parquet to fetch only needed data
- For DuckDB slowdowns, vacuum/compact the database or rebuild it

---

## 9. Still Stuck?

- Revisit setup steps: `docs/SETUP_GUIDE.md`
- Review SQL notebook instructions: `docs/SQL_ANALYTICS.md`
- Ask maintainers (see `docs/DEVELOPMENT.md` for contacts)


