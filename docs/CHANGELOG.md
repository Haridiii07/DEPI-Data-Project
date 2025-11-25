# Changelog

Documenting notable updates across milestones. Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) style where possible.

---

## [Unreleased]
- Database relocated from `scripts/` to `warehouse/` directory for better organization
- Updated all documentation to reflect new project structure (`src/etl/`, `src/dash/`, `warehouse/`)
- Fixed empty fact table issue in database build process
- Documentation split into dedicated guides (setup, parquet, SQL, dashboard, development, validation, troubleshooting)
- README streamlined to highlight key information and link to docs
- Updated CI/CD workflow with correct paths and proper testing pipeline

---

## [2025-11-20] Milestone 3 – Visualization & Dashboard

### Added
- Streamlit dashboard (`src/dash/app.py`) with interactive filters, attendance heatmaps, and trend charts
- Plotly heatmaps + Matplotlib/Seaborn visualizations in combined notebook
- Export buttons for CSV outputs (`output/` folder)

### Fixed
- Polish around Jupyter notebook to ensure repeatable execution

---

## [2025-11-13] Parquet Enhancement

### Added
- `src/etl/convert_to_parquet.py` for batch CSV → Parquet conversion
- `src/etl/assemble_dataset.py` updated to assemble Parquet batches + optional sample creation
- Documentation outlining Parquet benefits and workflow

### Changed
- Primary dataset artifacts now distributed as Parquet (`cleaned_students.parquet`, `sample_100K_students.parquet`)

---

## [2025-11-07] Milestone 2 – SQL Integration & Analytics

### Added
- DuckDB star schema (`student_performance.duckdb`)
- Advanced SQL analytics + visualizations notebook (`scripts/Milestone2_3_SQL_and_Visualizations.ipynb`)
- CSV exports: `subject_performance_analysis.csv`, `top_performers.csv`, `performance_by_university_type.csv`, `seasonal_performance_patterns.csv`
- ER diagram asset (`assets/ERD (Entity Relationship Diagram) based on the database design.png`)

---

## [2025-10-31] Milestone 1 – Data Preprocessing

### Added
- Batch cleaning pipeline (`real_data_milestone1.py`, `clean_students_batches.py`)
- Combined cleaned dataset (`cleaned_students.csv`)
- Initial data dictionary (`docs/data_dictionary.md`)

### Notes
- Large raw CSV deleted after cleaning to save space; cleaned batches retained

---

## Legacy Notes

For earlier planning artifacts (proposal, timeline, stakeholder analysis) see `docs/Proposal_ Student Performance Dashboard.md` and assets folder.


