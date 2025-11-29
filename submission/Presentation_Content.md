# 📊 Student Performance Dashboard - Presentation Content

> **Note:** Copy the content below into your PowerPoint slides.

---

## Slide 1: Title Slide
**Title:** Student Performance Dashboard
**Subtitle:** Interactive Analytics for Educational Insights
**Team:** Group 4 (DEPI Data Project)
**Members:**
- Abdulrahman Mustafa (Team Leader)
- Malak Samir
- Eman Wassem
- Khaled Ehab
- Ahmed Mohamed Galal Shoeib

---

## Slide 2: Problem Statement
**The Challenge:**
- Educational institutions collect massive amounts of data.
- Teachers and admins struggle to find actionable insights in raw spreadsheets.
- Identifying "at-risk" students happens too late.

**The Solution:**
- A centralized, interactive dashboard.
- Real-time visualization of grades, attendance, and trends.
- Early warning system for students needing support.

---

## Slide 3: Project Objectives
1.  **Scalability:** Process and analyze **1 Million+** student records.
2.  **Performance:** Deliver insights in **< 5 seconds** using in-memory analytics.
3.  **Usability:** Create an intuitive interface for non-technical users (teachers).
4.  **Accessibility:** Ensure data is accessible via a web-based platform (Streamlit Cloud).

---

## Slide 4: Architecture & Tech Stack
**Workflow:**
`Raw Data (CSV)` ➡️ `ETL Pipeline (Pandas)` ➡️ `Parquet Storage` ➡️ `DuckDB (Star Schema)` ➡️ `Streamlit Dashboard`

**Technologies:**
- **Python:** Core logic and scripting.
- **DuckDB:** High-performance in-memory SQL database.
- **Streamlit:** Interactive web application framework.
- **Plotly:** Dynamic and interactive charts.
- **GitHub Actions:** CI/CD for automated deployment.

---

## Slide 5: Data Pipeline (ETL)
**1. Extraction:**
- Combined real IPEDS institutional data with synthetic student records.
- Total Volume: 1,000,000 Students.

**2. Transformation:**
- Cleaned missing values and standardized formats.
- Modeled into a **Star Schema**:
    - **Fact Table:** Student Performance
    - **Dimensions:** Student, University, Course, Date

**3. Loading:**
- Saved as optimized **Parquet** files (90% smaller than CSV).

---

## Slide 6: Key Features - Overview
*(Insert Screenshot of "Overview" Tab)*

- **KPIs:** Instant view of Average Score (75.4), Attendance Rate (82.1%), and Pass Rate.
- **Distributions:** Histograms showing the spread of grades across the cohort.
- **Filters:** Slice data by Year, Major, or Subject instantly.

---

## Slide 7: Key Features - Risk Analysis
*(Insert Screenshot of "Risk Analysis" Tab)*

- **Correlation:** Scatter plot showing the strong link between Attendance and Scores.
- **At-Risk List:** Automatically flags students with:
    - Score < 60
    - Attendance < 70%
- **Actionable:** Teachers can download this list as a CSV to take action.

---

## Slide 8: Key Features - Student Profile
*(Insert Screenshot of "Student Profile" Tab)*

- **Individual Lookup:** Search for any student by ID.
- **360° View:** See a student's full academic history, grade trends over time, and specific subject performance.
- **Use Case:** Parent-teacher conferences or academic advising sessions.

---

## Slide 9: Challenges & Solutions
| Challenge | Solution |
|-----------|----------|
| **Big Data (1M Rows)** | Used **DuckDB** and **Parquet** for fast, columnar processing. |
| **GitHub Limits (100MB)** | Split large files (`.part1`, `.part2`) and stitched them automatically. |
| **Cloud Memory** | Created a lightweight **10K Sample** specifically for the live demo. |

---

## Slide 10: Future Work
- **Predictive Models:** Add Machine Learning to predict future grades.
- **Real-Time Data:** Connect to live LMS (Learning Management Systems).
- **Mobile App:** Optimize the layout for mobile devices.

---

## Slide 11: Thank You!
**Live Demo:** [https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/](https://depi-data-project-sxczyh8wks5x4bdwjznwgw.streamlit.app/)

**Q&A**
