# 🎓 Student Performance Dashboard

An interactive analytics platform for analyzing 1 million student records across 50 U.S. universities (2010–2024). Built with Python, DuckDB, and Streamlit.

![Status](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-Educational-orange)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
git clone <repository-url>
cd "Data Project"
pip install -r requirements.txt
```

### 2. Launch the Dashboard
```bash
python -m streamlit run src/dash/app.py
```

That's it! The app will automatically:
- ✅ Detect if the database exists
- ✅ Build it from the data if needed (~2-3 minutes first time)
- ✅ Open in your browser at http://localhost:8501

### Optional: Run Analytics Notebook
```bash
jupyter notebook "notebooks/Milestone2_3_SQL_and_Visualizations.ipynb"
```

📖 **Need more details?** Check the [Setup Guide](docs/SETUP_GUIDE.md) for advanced options.

---

## ✨ What You Get

- 📊 **1M Student Records** - Real university data + synthetic student performance
- ⚡ **Interactive Dashboard** - Filter by university, subject, semester, performance
- 📈 **Rich Visualizations** - Heatmaps, trends, distributions, correlations
- 🗄️ **Fast Analytics** - DuckDB star schema for sub-second queries
- 📁 **Efficient Storage** - Parquet format (75MB vs 1.6GB CSV)

---

## 📂 Project Structure

```
Data Project/
│
├── 📁 src/                          # Source code
│   ├── dash/                        # Dashboard application
│   │   └── app.py                   # Main Streamlit app
│   ├── etl/                         # Data processing scripts
│   │   ├── real_data_milestone1.py  # Generate 1M student records
│   │   ├── clean_students_batches.py # Data cleaning
│   │   ├── build_database.py        # Create DuckDB database
│   │   └── majors_config.py         # Academic major configurations
│   └── tools/                       # Utility tools
│       └── ipeds-scraper/           # IPEDS data downloader
│
├── � data/                         # Data files
│   └── processed/                   # Cleaned data (Parquet format)
│       └── milestone1_real/         
│           └── cleaned_students.parquet  # Main dataset (75MB)
│
├── 📁 warehouse/                    # Database storage (auto-created)
│   └── student_performance.duckdb   # DuckDB database (~180MB, git-ignored)
│
├── 📁 docs/                         # Documentation
│   ├── SETUP_GUIDE.md              # Detailed setup instructions
│   ├── DASHBOARD_GUIDE.md          # How to use the dashboard
│   ├── SQL_ANALYTICS.md            # SQL queries and analytics
│   ├── PARQUET_GUIDE.md            # Data format explanation
│   ├── TROUBLESHOOTING.md          # Common issues and fixes
│   ├── VALIDATION.md               # Data validation commands
│   ├── DEVELOPMENT.md              # Contributor guide
│   ├── CHANGELOG.md                # Version history
│   ├── data_dictionary.md          # Column definitions
│   └── assets/                     # Images (ERD, wireframes, timeline)
│
├── 📁 notebooks/                    # Jupyter notebooks
│   └── Milestone2_3_SQL_and_Visualizations.ipynb
│
├── 📁 analytics/                    # Exported analysis results
│   └── exports/                    # CSV outputs from queries
│
├── 📁 tests/                        # Test suite
│   └── test_data_validation.py     # Data integrity tests
│
├── 📜 requirements.txt              # Python dependencies
├── 📜 pyproject.toml               # Project configuration
└── 📜 README.md                    # You are here!
```

### Key Directories Explained

| Directory | Purpose | Important Files |
|-----------|---------|----------------|
| `src/dash/` | Dashboard UI | `app.py` - Run this to start the app |
| `src/etl/` | Data pipeline | `build_database.py` - Creates the database |
| `data/processed/` | Clean data | `cleaned_students.parquet` - 1M student records |
| `warehouse/` | Database | Auto-created when you run the app |
| `docs/` | Documentation | Start with `SETUP_GUIDE.md` |

---

## 📊 Features

### Dashboard Capabilities
- 🎯 **KPI Overview** - Average scores, attendance rates, pass rates
- 🔍 **Smart Filters** - By university type, subject, semester, date range
- 📈 **Visualizations**
  - Performance distributions
  - Attendance heatmaps
  - Score trends over time
  - Subject comparisons
- 💾 **Export Data** - Download filtered results as CSV

### Technical Features
- **Fast Performance** - Parquet + DuckDB = 10-50× faster than CSV
- **Star Schema** - Optimized for analytics queries
- **Auto-Setup** - Database builds automatically on first run
- **Test Suite** - Automated data validation with pytest

---

## 📚 Documentation

Start here based on what you need:

| I want to... | Read this |
|--------------|-----------|
| 🚀 Set up the project | [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) |
| 🎨 Use the dashboard | [DASHBOARD_GUIDE.md](docs/DASHBOARD_GUIDE.md) |
| 🗄️ Understand the database | [SQL_ANALYTICS.md](docs/SQL_ANALYTICS.md) |
| 📁 Learn about Parquet format | [PARQUET_GUIDE.md](docs/PARQUET_GUIDE.md) |
| 🐛 Fix a problem | [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| ✅ Validate data | [VALIDATION.md](docs/VALIDATION.md) |
| 🤝 Contribute | [DEVELOPMENT.md](docs/DEVELOPMENT.md) |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Database**: DuckDB (embedded analytics database)
- **Data Format**: Apache Parquet (columnar storage)
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest

---

## � Milestones

| Milestone | Status | Description |
|-----------|--------|-------------|
| M1: Data Preprocessing | ✅ Complete | 1M student records generated and cleaned |
| M2: SQL Analytics | ✅ Complete | Star schema database with advanced queries |
| M3: Visualization | ✅ Complete | Interactive Streamlit dashboard |
| M4: Documentation | 🚧 In Progress | Final documentation and guides |

---

## 🤝 Contributing

We welcome contributions! Please:

1. Read [DEVELOPMENT.md](docs/DEVELOPMENT.md) for coding standards
2. Run tests before submitting: `pytest`
3. Update [CHANGELOG.md](docs/CHANGELOG.md) with your changes
4. Keep commits focused and well-documented

---

## ❓ Need Help?

- 📖 Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues
- 🐛 Found a bug? Open an issue
- 💡 Have a question? See the documentation guides above

---

## 📄 License

Educational and research purposes only. Data combines public IPEDS sources with synthetic student records.

---

**Built with ❤️ for data analytics education**
