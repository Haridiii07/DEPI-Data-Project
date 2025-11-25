# Setup Guide

Comprehensive instructions for preparing the Student Performance Dashboard environment across Windows (PowerShell) and macOS/Linux (bash). Follow the sections in order; advanced tasks are optional.

---

## 1. Prerequisites

- Python 3.8+ (verify via `python --version`)
- Git (optional but recommended)
- 16 GB RAM recommended for full 1M-row dataset; sample dataset works on 8 GB machines
- `pip` for dependency installation

---

## 2. Clone the Repository

```bash
git clone <repository-url>
cd "Data Project"
```

If you already have the files, ensure you are at the project root that contains `README.md`, `src/`, and `data/`.

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you manage multiple Python versions, prefer `python -m pip install -r requirements.txt`.

---

## 4. Prepare the Dataset

### 4.1 Convert CSV to Parquet (recommended)

```bash
python src/etl/convert_to_parquet.py
```

- Discovers `students_batch_XX_100K_cleaned.csv`
- Writes `.parquet` versions next to each CSV
- Preserves the original CSV files for compatibility

### 4.2 Assemble the Full Dataset

```bash
python src/etl/assemble_dataset.py
```

What it does:
- Scans `data/processed/milestone1_real/` for `students_batch_01_100K_cleaned.parquet` … `students_batch_10_100K_cleaned.parquet`
- Concatenates batches in numeric order
- Saves `data/processed/milestone1_real/cleaned_students.parquet`

**Optional:** create a reproducible sample (10K rows per batch by default)

```bash
python src/etl/assemble_dataset.py --create-sample --rows-per-batch 10000
```

### 4.3 Recreate Raw Data (optional)

Use only if you need to regenerate the cleaned batches from raw IPEDS inputs:

```bash
python src/etl/real_data_milestone1.py
python src/etl/clean_students_batches.py
```

Then rerun the Parquet conversion and assembly steps above.

---

## 5. Build the DuckDB Database (Milestone 2)

```bash
python src/etl/build_database.py
```

> **Note:** The Streamlit dashboard (`src/dash/app.py`) will automatically run this script if the database is missing. You only need to run this manually if you want to rebuild the database explicitly.

- Creates `warehouse/student_performance.duckdb`
- Implements the star schema (4 dimension tables + 1 fact table)
- Processes 10M+ records in seconds on a typical laptop

---

## 6. Run Analytics Notebook (Milestones 2 & 3)

```bash
jupyter notebook "notebooks/Milestone2_3_SQL_and_Visualizations.ipynb"
```

PowerShell variant:

```powershell
jupyter notebook "notebooks\Milestone2_3_SQL_and_Visualizations.ipynb"
```

Notebook outputs:
- Advanced SQL queries with DuckDB
- ER diagram generation
- Multiple visualizations (matplotlib, seaborn)
- CSV exports written to `output/`

---

## 7. Launch the Streamlit Dashboard (Milestone 3)

```bash
python -m streamlit run src/dash/app.py
```

Access the UI at http://localhost:8501. The app reads directly from DuckDB and Parquet sources for real-time filtering.

---

## 8. Dataset Utilities

### Sample Dataset

```bash
python src/etl/create_sample_dataset.py
python src/etl/verify_sample.py
```

Compress sample for sharing (PowerShell):

```powershell
Compress-Archive -Path data/processed/milestone1_real/sample_100K_students.csv `
  -DestinationPath data/processed/milestone1_real/sample_100K_students.zip -Force
```

### Batch Validation Quick Commands

See `docs/VALIDATION.md` for row-count checks, schema assertions, and troubleshooting tips.

---

## 9. Environment Tips

- Prefer forward slashes (`src/etl/assemble_dataset.py`) in documentation; PowerShell accepts them.
- Set `PYTHONPATH` or run commands from repo root to avoid import errors.
- For Apple Silicon, install the `duckdb` wheel that matches your architecture (`pip install duckdb==0.9.2` or newer).

---

## 10. Need Help?

- Troubleshooting guide: `docs/TROUBLESHOOTING.md`
- Dashboard usage details: `docs/DASHBOARD_GUIDE.md`
- Contact maintainers listed in `docs/DEVELOPMENT.md`


