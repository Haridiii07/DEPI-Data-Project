# 🎓 Student Performance Dashboard

Holistic analytics platform for 1M students across 50 U.S. universities (2010–2024). The repository covers data preprocessing, Parquet conversion, DuckDB star schema analytics, and an interactive Streamlit dashboard.

**Status:** ✅ Milestones 1‑3 complete · 🚧 Milestone 4 (final documentation) in progress  
**Quick links:** [Setup](docs/SETUP_GUIDE.md) · [Parquet](docs/PARQUET_GUIDE.md) · [SQL & Analytics](docs/SQL_ANALYTICS.md) · [Dashboard](docs/DASHBOARD_GUIDE.md) · [Contributing](docs/DEVELOPMENT.md)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Milestone Status](#-milestone-status)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Technology Stack](#-technology-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📘 Overview

- Dataset size: 1M students · 9.9M+ performance records · 2010–2024 coverage  
- Pipeline: batch cleaning scripts, deterministic sampling, Parquet-first storage  
- Analytics: DuckDB fact/dimension schema + advanced SQL queries + CSV exports  
- Visualization: Streamlit dashboard, Matplotlib/Seaborn/Plotly charts, wireframes and ERD stored under `assets/`

Planning artifacts (stakeholders, risks, ERD drafts) are compiled in `docs/Proposal_ Student Performance Dashboard.md`, with supporting visuals in `assets/ERD (Entity Relationship Diagram) based on the database design.png`, `assets/TimelineGantt chart for the project plan.png`, and `assets/wireframes for the UIUX design.png`.

---

## 🚀 Quick Start

```bash
git clone <repository-url>
cd "Data Project"
pip install -r requirements.txt

python scripts/convert_to_parquet.py
python scripts/assemble_dataset.py
python scripts/build_database.py

jupyter notebook "scripts/Milestone2_3_SQL_and_Visualizations.ipynb"
python -m streamlit run dashboard/app.py
```

- Need PowerShell-specific paths, optional sampling, or regeneration steps? See `docs/SETUP_GUIDE.md`.
- Validation commands and sanity checks live in `docs/VALIDATION.md`.

---

## ✨ Features

- **📊 Large-scale dataset:** Cleaned, standardized data for 50 universities, 31 subjects, and 1M students
- **⚡ Parquet-first storage:** ~95% compression, column-pruning reads, CSV compatibility preserved
- **🗄️ DuckDB star schema:** Sub-second analytics using fact + 4 dimension tables
- **📈 Analytics exports:** Subject benchmarks, attendance trends, correlation insights, seasonal patterns
- **🎨 Interactive dashboard:** Streamlit app with KPI tiles, filters, attendance heatmaps, CSV download buttons
- **🧭 Documentation suite:** Dedicated guides for setup, analytics, validation, troubleshooting, and development workflow

Deep dives: `docs/PARQUET_GUIDE.md` and `docs/SQL_ANALYTICS.md`.

---

## 📊 Milestone Status

| Milestone | Deadline | Status | Highlights |
|-----------|----------|--------|------------|
| M1: Data Preprocessing | Oct 31, 2025 | ✅ Complete | Batch cleaning, Parquet datasets, data dictionary |
| M2: SQL Analytics | Nov 7, 2025 | ✅ Complete | DuckDB star schema, ERD, analytics notebook, CSV exports |
| M3: Visualization | Nov 20, 2025 | ✅ Complete | Streamlit dashboard, attendance heatmaps, trend charts |
| M4: Documentation | Dec 1, 2025 | 🚧 In Progress | Final docs, report, presentation assets |

Full history is tracked in `docs/CHANGELOG.md`. The project timeline graphic resides at `assets/TimelineGantt chart for the project plan.png`.

---

## 🏗️ Project Structure

```
Data Project/
├── data/                # Parquet datasets, samples (large CSVs ignored via .gitignore)
├── scripts/             # ETL scripts + Milestone 2&3 notebook
├── dashboard/           # Streamlit app and prototype files
├── docs/                # Guides, changelog, proposal, data dictionary
├── assets/              # ERD, timeline, wireframes
├── output/              # Generated CSV analytics
├── tests/               # Pytest suite
├── requirements.txt
└── README.md
```

See `docs/DEVELOPMENT.md` for a script catalog and repo hygiene expectations. Column definitions are documented in `docs/data_dictionary.md`.

---

## 📚 Documentation

| Topic | Reference |
|-------|-----------|
| Environment & setup steps | `docs/SETUP_GUIDE.md` |
| Parquet rationale & workflow | `docs/PARQUET_GUIDE.md` |
| SQL analytics & DuckDB schema | `docs/SQL_ANALYTICS.md` |
| Dashboard usage & UX references | `docs/DASHBOARD_GUIDE.md` |
| Contributor workflow & standards | `docs/DEVELOPMENT.md` |
| Data validation commands | `docs/VALIDATION.md` |
| Troubleshooting & FAQ | `docs/TROUBLESHOOTING.md` |
| Release history | `docs/CHANGELOG.md` |
| Data dictionary | `docs/data_dictionary.md` |
| Proposal & stakeholder plan | `docs/Proposal_ Student Performance Dashboard.md` |

Each guide links to related documents so readers can move between beginner and advanced content quickly.

---

## 🛠️ Technology Stack

- **Languages & libs:** Python 3.8+, pandas, PyArrow, DuckDB, Streamlit, Matplotlib, Seaborn, Plotly
- **Storage:** Apache Parquet for datasets, DuckDB for analytics
- **Tooling:** Jupyter Notebook, pytest, Git/GitHub
- **Assets:** ERD, timeline, and UI wireframes stored under `assets/`

---

## 🤝 Contributing

- Follow the practices in `docs/DEVELOPMENT.md` (PEP 8, type hints, tidy notebooks)
- Keep README concise—move detailed instructions into the docs suite
- Update `docs/CHANGELOG.md` whenever you add features or restructure docs
- For UI changes, include updated screenshots in `assets/`
- Run relevant validation/tests before submitting PRs (`pytest`, scripts from `docs/VALIDATION.md`)

---

## 📄 License

Educational and research purposes only. Data combines public IPEDS sources with synthetic student records. For questions, open an issue or contact the maintainers listed in the proposal document.


