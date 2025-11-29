# 🎓 Student Performance Dashboard

## 🌟 Project Overview
The **Student Performance Dashboard** is a comprehensive analytics platform designed to help educational institutions, teachers, and administrators analyze student performance data effectively. Built using **Python**, **Streamlit**, and **DuckDB**, the system processes over **1 million student records** to provide actionable insights into grades, attendance, and risk factors.

## 🚀 Key Features

### 1. Interactive Dashboard
- **Overview Tab:** Displays high-level KPIs (Average Score, Attendance Rate, Pass Rate) and visualizations for quick performance assessment.
- **Subject & Cohort Analysis:** Deep dive into specific subjects and student cohorts with interactive heatmaps and trend charts.
- **Risk Analysis:** Automatically identifies at-risk students (Score < 60 or Low Attendance) and visualizes the correlation between attendance and grades.
- **Student Profile:** A dedicated lookup tool to view detailed academic history for any individual student (1-10,000 in cloud sample).

### 2. Robust Data Pipeline (ETL)
- **Data Collection:** Integrates real institutional data from IPEDS with algorithmically generated student records.
- **Data Cleaning:** Automated scripts (`src/etl/`) clean, standardize, and anonymize data, ensuring high data quality.
- **Star Schema:** Transforms raw data into an optimized Star Schema (Fact/Dimension tables) for efficient analytical querying.
- **Parquet Storage:** Uses columnar Parquet files for high-performance data storage and retrieval, reducing file sizes by 90%.

### 3. Cloud & Local Flexibility
- **Cloud Optimized:** Deploys seamlessly to Streamlit Cloud using a lightweight 10K student sample (0.78 MB).
- **Local Power:** Scales to the full 1M student dataset (72 MB) when run locally, with automatic data stitching and schema generation.

## 🛠️ Technology Stack
- **Frontend:** Streamlit (Python)
- **Database:** DuckDB (In-memory OLAP)
- **Data Processing:** Pandas, NumPy
- **Storage:** Apache Parquet
- **Visualization:** Plotly Express
- **Version Control:** Git & GitHub

## 🔗 Live Demo
Access the live application here:  
**[Student Performance Dashboard](https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/)**

## 👥 Team Members
- **Abdulrahman Mustafa** (Team Leader)
- **Malak Samir**
- **Eman Wassem**
- **Khaled Ehab**
- **Ahmed Mohamed Galal Shoeib**

---
*Submitted as part of the Digital Egypt Pioneers Initiative (DEPI) Final Project.*
