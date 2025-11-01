# Proposal: Student Performance Dashboard

**Deliverable for Ministry LMS Submission**

**Team Name:** Group 4
**Team Leader:** Abdulrahman Mustafa
**Date:** November 1, 2025

**Submission Note:** This Proposal compiles the project planning, stakeholder analysis, database design, and UI/UX drafts required for the Graduation Project assignment. A link to the code repository and supporting visuals are included.

---

## 1) Project Planning

**Project Title:** Student Performance Dashboard

**Problem Statement:** Schools collect large volumes of student records but lack a consolidated analytics tool to detect trends in grades and attendance. This project builds an ETL + analytics dashboard that surfaces actionable insights for teachers and admins.

**Vision & Objectives:**
*   **Support Analysis of 10M+ Records:** Implement a scalable data pipeline capable of processing and storing over 10 million student records efficiently.
*   **Fast Dashboard Performance:** Ensure the dashboard's initial load and core view rendering is fast, targeting under 5 seconds on a reasonable local machine.
*   **Visualize Key Trends:** Create clear, interactive visualizations to track attendance, grade trends, and identify top/low performers.
*   **Deliver Full Documentation:** Provide comprehensive documentation and a stakeholder-ready presentation for project handoff.

**Scope (In-scope / Out-of-scope):**

| In-Scope | Out-of-Scope |
| :--- | :--- |
| ETL pipeline for data cleaning and standardization. | Real-time data streaming or live data ingestion. |
| Normalized SQL database design and population. | Advanced machine learning models for predictive analytics. |
| Interactive dashboard with core KPIs and visualizations. | Full production deployment on a cloud platform (focus on local/test environment). |

**Tools & Technologies:**
*   **Core:** Python (Pandas), Parquet, DuckDB / PostgreSQL, Matplotlib / Seaborn / Plotly, Git/GitHub.
*   **Dashboard:** Streamlit (or Plotly Dash).

**Timeline (Milestone Summary):**

| Milestone | Deliverables | Deadline |
| :--- | :--- | :--- |
| **M1: Data Preprocessing** | Cleaned dataset (Parquet), ETL scripts, data dictionary. | Oct 31, 2025 |
| **M2: SQL Integration** | Database schema, loaded tables, tested queries (notebook). | Nov 7, 2025 |
| **M3: Visualization** | Visualization notebook + interactive dashboard. | Nov 20, 2025 |
| **M4: Presentation** | Final report (PDF) + slide deck + demo. | Dec 1, 2025 |

**Top Risks & Mitigations:**

| Risk | Mitigation |
| :--- | :--- |
| **Data Size / Compute Limits:** Processing 10M+ records may exceed local memory/CPU. | Use batch processing (already implemented in M1) and Parquet for efficient storage/reading. Utilize DuckDB for fast local analytical queries. |
| **Missing/Poor-Quality Data:** Inconsistencies in the raw dataset. | Implement robust data cleaning and validation scripts (`clean_students_batches.py`) with clear logging and data quality KPIs (Target: 100% handling of duplicates/nulls). |
| **Dashboard Stability:** Interactive dashboard is complex to deploy and maintain. | Prioritize a simple, stable framework (Streamlit) and ensure all data loading is pre-optimized via the SQL database (M2). |

---

## 2) Stakeholder Analysis

The project's success is measured by its utility to the primary stakeholders.

| Stakeholder | Primary Needs | RACI (Core Deliverables) | Success Metrics |
| :--- | :--- | :--- | :--- |
| **Teachers** | Quick identification of at-risk students and grade trends. | **R**esponsible for Dashboard, **C**onsulted on UI/UX. | Teacher usefulness score (Target: ≥ 4/5). |
| **School Admins** | High-level performance summaries and cohort comparisons. | **A**ccountable for Project Success, **I**nformed on all milestones. | Admin time saved in generating reports. |
| **Students/Guardians** | Clear, understandable view of individual performance. | **I**nformed on final report/dashboard. | Student support leads identified. |
| **IT Staff** | Stable, maintainable, and scalable data pipeline. | **C**onsulted on DB Design, **R**esponsible for Data Preprocessing. | ETL throughput and storage efficiency KPIs met. |
| **Project Mentors** | Adherence to data engineering best practices and project objectives. | **C**onsulted on all technical decisions. | Final report and presentation score (Target: ≥ 4/5). |

**RACI Matrix (Team Members):**

| Deliverable | Abdulrahman (DE) | Malak (DE/DA) | Khaled (DA/Viz/TL) | Eman (Doc/Pres) | Ahmed (Doc/Pres) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Data Preprocessing | **R** | **R** | **C** | **I** | **I** |
| DB Design | **A** | **R** | **C** | **I** | **I** |
| Dashboard/Viz | **C** | **C** | **R** | **I** | **I** |
| Final Report | **C** | **C** | **C** | **R** | **R** |

---

## 3) Database Design

**Summary:** The database's purpose is to provide a normalized, queryable structure for the cleaned student performance data. It moves the data from flat files (Parquet) into a relational model to support fast, complex analytical queries required for the dashboard.

**Main Entities:** The core entities are **Students**, **Subjects**, **Scores**, and **Attendance**.

**Schema Snapshot (Key Tables):**

| Table Name | Key Attributes | Description |
| :--- | :--- | :--- |
| **Students** | `student_id` (PK), `given_name`, `family_name`, `cohort_id` | Unique student records and demographic data. |
| **Subjects** | `subject_id` (PK), `name` | List of all subjects offered. |
| **Scores** | `score_id` (PK), `student_id` (FK), `subject_id` (FK), `score_value` | Individual score records for each student/subject. |
| **Attendance** | `att_id` (PK), `student_id` (FK), `date`, `status` | Daily attendance records (e.g., Present, Absent, Tardy). |

**Relationships & Indexing Notes:**
*   **Primary Keys (PK):** Surrogate keys (`student_id`, `subject_id`, `score_id`, `att_id`) are used for all tables to ensure uniqueness and stability.
*   **Foreign Keys (FK):** `Scores` and `Attendance` link back to `Students` via `student_id`. `Scores` also links to `Subjects` via `subject_id`.
*   **Indexing:** Columns frequently used in `WHERE` clauses or `JOIN` conditions will be indexed for performance. Key indexes include: `student_id` (on `Scores` and `Attendance`), `date` (on `Scores` and `Attendance`), and `subject_id` (on `Scores`).

**Data Volume Note & Storage Format:**
The raw data is approximately 10 million records. The ETL process uses **Apache Parquet** for efficient, columnar storage of the cleaned dataset, which significantly reduces file size and improves read performance. The final analytical database will be implemented using **DuckDB** (for fast local analytics) or **PostgreSQL** (for a more robust relational environment).

**ERD:**
*(Placeholder for Embedded ERD PNG)*

---

## 4) UI / UX Design

**Key Screens Required:**

1.  **Overview / Landing:** The primary screen for administrators and teachers. It will feature key performance indicators (KPIs) like overall attendance rate, average score, and a quick filter panel (by cohort, subject, and time range).
2.  **Student Profile:** A detailed view for individual students. It will display a grade history timeline, attendance log, and a summary of performance categories.
3.  **Cohort / Trend Analysis:** A screen dedicated to comparative analysis. It will feature trend charts (e.g., average score over time for different cohorts) and heatmaps to visualize subject performance distribution.

**User Flow (Filter → Inspect → Act):**

1.  **Filter:** A teacher filters the Overview screen by "Cohort 2024" and "Math" subject.
2.  **Inspect:** The teacher notices a dip in the average score trend chart and clicks on a specific student's name to inspect their detailed **Student Profile**.
3.  **Act:** Based on the detailed profile, the teacher identifies the student is missing key assignments and schedules a follow-up meeting.

**Wireframes:**
*(Placeholder for Embedded Wireframe 1: Overview Dashboard)*
*(Placeholder for Embedded Wireframe 2: Student Profile)*
*(Placeholder for Embedded Wireframe 3: Cohort Trend Analysis)*

**Accessibility & Audience Notes:**
The design will prioritize **clarity** and **readability**. We will use clear labels, a high-contrast color palette that is **color-blind friendly**, and readable, professional fonts. The dashboard is designed for both technical (IT Staff) and non-technical (Teachers, Admins) users, ensuring that complex data is presented with simple, actionable interpretations.

---

## Appendix / Attachments

### Code Repository Citation

The project’s codebase and ETL scripts are available in the team’s GitHub repository:
**[https://github.com/Haridiii07/DEPI-Data-Project](https://github.com/Haridiii07/DEPI-Data-Project)**

**Key referenced files:**
*   `scripts/clean_students_batches.py`
*   `scripts/assemble_dataset.py`
*   `README.md`

**How to Access Code (for Evaluators):**
The repository contains all necessary scripts and a sample dataset. Evaluators can clone the repository and run `pip install -r requirements.txt` followed by `python scripts/assemble_dataset.py` to recreate the full cleaned dataset locally.

### Sources & Tools

*   **Python:** CPython / official docs
*   **Pandas:** Data cleaning & ETL
*   **Apache Parquet / Apache Arrow:** Storage format
*   **DuckDB / PostgreSQL:** Analytical database
*   **Matplotlib / Seaborn / Plotly:** Visualization libraries
*   **Streamlit / Plotly Dash:** Interactive dashboard framework
*   **Git / GitHub:** Version control & code repo
*   **Diagram Tools:** draw.io / dbdiagram.io (for ERD)
*   **Wireframe Tools:** Figma / pen-and-paper (for mockups)

### Visuals (To be inserted as PNGs)

*   ERD image (PNG)
*   2–3 wireframe PNGs
*   Timeline/Gantt image (from Project Planning section)
