# 🎓 Student Performance Dashboard

<div align="center">

### Interactive Analytics Platform for Student Data

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](https://github.com/Haridiii07/DEPI-Data-Project)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-orange?style=for-the-badge)](LICENSE)

**Analyze student performance across universities with powerful visualizations and insights**

[Features](#-features) • [Live Demo](#-live-demo) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 🌟 Overview

A comprehensive analytics dashboard for student performance data, featuring:
- **1 Million Students** - Full dataset for local analysis
- **10,000 Students** - Optimized cloud deployment
- **Real-time Filtering** - By major, subject, year
- **Interactive Visualizations** - Charts, heatmaps, distributions
- **Risk Analysis** - Identify at-risk students
- **Individual Profiles** - Detailed student lookup

Built with **Python**, **DuckDB**, **Streamlit**, and **Plotly** for fast, interactive data exploration.

---

## 🎯 Features

### 📊 **Overview Dashboard**
- Key Performance Indicators (KPIs)
- Average scores, attendance rates, pass rates
- Score distribution histograms
- Performance by major bar charts

### 📚 **Subject & Cohort Analysis**
- Top performing subjects
- Interactive attendance heatmaps
- Subject-major cross-analysis
- Filter by year/semester

### 🚨 **Risk Analysis**
- Identify at-risk students (score < 60 or low attendance)
- Scatter plot visualizations
- Downloadable CSV reports
- Predictive indicators

### 👤 **Student Profile**
- Search by student number (1-10,000 on cloud)
- Individual academic history
- Course performance timeline
- Detailed grade breakdown

---

## 🌐 Live Demo

**Try it now:** [https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/](https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/)

The live demo uses a 10K student sample optimized for Streamlit Cloud's free tier.

---

## 🚀 Quick Start

### Cloud Version (Recommended)
Simply visit the [live demo](https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/) - no installation required!

### Local Installation

#### Prerequisites
- Python 3.8 or higher
- Git

#### Steps

1. **Clone the repository**
```bash
git clone https://github.com/Haridiii07/DEPI-Data-Project.git
cd DEPI-Data-Project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run src/dash/app.py
```

The dashboard will open automatically at `http://localhost:8501`

> **Note:** First load may take 30-60 seconds as it builds the star schema from the 1M student dataset.

---

## 📂 Project Structure

```
DEPI-Data-Project/
├── src/
│   ├── dash/
│   │   └── app.py                    # Main Streamlit dashboard
│   └── etl/
│       ├── generate_star_schema.py   # Star schema generator
│       ├── create_cloud_sample.py    # 10K sample creator
│       ├── split_data.py             # File splitter utility
│       └── majors_config.py          # Academic configuration
│
├── data/
│   ├── sample_50K_students.parquet   # Cloud sample (0.78 MB)
│   ├── cleaned_students.parquet.part1 # Local data part 1
│   ├── cleaned_students.parquet.part2 # Local data part 2
│   └── star_schema/                  # Generated schema (gitignored)
│
├── docs/
│   ├── DEPLOYMENT.md                 # Deployment guide
│   ├── DASHBOARD_GUIDE.md            # User guide
│   ├── CHANGELOG.md                  # Version history
│   └── README.md                     # Documentation index
│
├── tests/                            # Test suite
├── .github/workflows/                # CI/CD pipelines
└── requirements.txt                  # Python dependencies
```

---

## 💡 How It Works

### Data Pipeline

1. **Raw Data** → Cleaned student records (1M students, 10M+ records)
2. **Parquet Format** → Columnar storage for efficient querying
3. **Star Schema** → DuckDB optimized structure
4. **Streamlit Dashboard** → Interactive visualization

### Cloud vs Local

| Feature | Cloud | Local |
|---------|-------|-------|
| Students | 10,000 | 1,000,000 |
| Data Size | 0.78 MB | 72 MB |
| Load Time | ~5s | ~30s |
| Search Range | 1-10,000 | All students |

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Database:** DuckDB (in-memory analytics)
- **Data Format:** Apache Parquet
- **Visualization:** Plotly, Matplotlib
- **Data Processing:** Pandas, NumPy
- **Deployment:** Streamlit Cloud
- **CI/CD:** GitHub Actions

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Cloud and local deployment guide |
| [DASHBOARD_GUIDE.md](docs/DASHBOARD_GUIDE.md) | How to use the dashboard features |
| [CHANGELOG.md](docs/CHANGELOG.md) | Version history and updates |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Contributor guide |

---

## 🎓 Use Cases

- **Educational Institutions:** Monitor student performance trends
- **Data Analysts:** Practice with real-world educational data
- **Researchers:** Study performance patterns and correlations
- **Developers:** Learn Streamlit, DuckDB, and data visualization

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed guidelines.

---

## 📊 Data Information

- **Dataset:** 1,000,000 students across 30 universities
- **Time Period:** Academic year 2022
- **Records:** ~10 million course enrollments
- **Majors:** 62 different academic programs
- **Subjects:** 100+ different courses
- **Format:** Parquet (compressed columnar storage)

---

## 🔐 Privacy & Ethics

This dataset combines:
- **Public IPEDS data** - University institutional data
- **Synthetic student records** - Algorithmically generated performance data

No real student privacy information is included. All data is for **educational and research purposes only**.

---

## 📝 License

This project is for **educational purposes**. The data combines public institutional data with synthetic student records generated for academic analysis.

---

## 👨‍💻 Authors

**DEPI Data Project Team**
- Built as part of the Digital Egypt Pioneers Initiative (DEPI)
- Contact: [GitHub Repository](https://github.com/Haridiii07/DEPI-Data-Project)

---

## 🙏 Acknowledgments

- **IPEDS** - Integrated Postsecondary Education Data System
- **Streamlit** - Amazing framework for data apps
- **DuckDB** - Fast in-process analytical database
- **DEPI Program** - Digital Egypt Pioneers Initiative

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

[![GitHub stars](https://img.shields.io/github/stars/Haridiii07/DEPI-Data-Project?style=social)](https://github.com/Haridiii07/DEPI-Data-Project/stargazers)

Made with ❤️ for data analytics education

</div>
