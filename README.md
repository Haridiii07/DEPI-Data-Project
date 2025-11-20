# Student Performance Data Project

## Overview

This repository contains **Milestone 1, 2, and 3** deliverables for the Student Performance Dashboard project.  
It provides a fully preprocessed, large-scale dataset of **1 million students** from the **top 50 U.S. universities** (2010–2024), with advanced SQL analytics, star schema database implementation using DuckDB, and an interactive Streamlit dashboard for optimal performance and visualization.

## Table of Contents

- [Folder Structure](#folder-structure)
- [Contents](#contents)
- [How to Use](#how-to-use)
- [Milestone 2: SQL Integration & Analytics](#milestone-2-sql-integration--analytics)
- [Why Parquet? 🚀](#why-parquet-)
- [Dataset Access (Google Drive)](#dataset-access-google-drive)
- [Sample Dataset (100K Students)](#sample-dataset-100k-students)
- [Data Details](#data-details)
- [Validation (Quick Checks)](#validation-quick-checks)
- [What We Did (Changelog)](#what-we-did-changelog)
- [Project Timeline & Planning](#project-timeline--planning-)
- [UI/UX Design & Dashboard Wireframes](#uiux-design--dashboard-wireframes-)
- [Next Steps for the Team](#next-steps-for-the-team)
- [License](#license)

---

## Folder Structure

```text
Data Project/
├── data/
│   └── milestone1_real/
│       ├── students_batch_01_100K_cleaned.parquet  # Parquet versions (95% smaller!)
│       ├── ... (up to students_batch_10_100K_cleaned.parquet)
│       ├── sample_100K_students.parquet        # Sample dataset (Parquet)
│       ├── summary_1M_real_data.parquet        # Summary stats
│       └── cleaned_students.parquet            # Assembled full Parquet (generated locally)
├── scripts/
│   ├── real_data_milestone1.py                 # Generates original dataset from IPEDS
│   ├── clean_students_batches.py              # Cleans and standardizes batch data
│   ├── create_sample_dataset.py                # Creates 100K-student sample from batches
│   ├── verify_sample.py                        # Verifies sample dataset stats
│   ├── assemble_dataset.py                    # Assembles Parquet batches → single Parquet
│   ├── convert_to_parquet.py                  # Converts CSV files to Parquet format
│   ├── generate_summary.py                    # Generates summary statistics
│   ├── Milestone2_3_SQL_and_Visualizations.ipynb   # Milestones 2 & 3: SQL + Visualizations
│   └── student_performance.duckdb              # DuckDB database file
├── output/
│   └── subject_performance.csv                # Generated analytical outputs
├── docs/                                       # Documentation and proposals
│   ├── Proposal_ Student Performance Dashboard.md
│   ├── data_dictionary.md                      # Data dictionary (16 columns)
│   └── *.pdf                                   # Additional documentation PDFs
├── assets/                                     # Visual assets and diagrams
│   ├── ERD (Entity Relationship Diagram) based on the database design.png
│   ├── TimelineGantt chart for the project plan.png
│   └── wireframes for the UIUX design.png
├── dashboard/                                  # Dashboard UI components
│   ├── app.py                                 # Streamlit dashboard (M3)
│   └── edu-analytics-dashboard.tsx             # React prototype (unused)
├── requirements.txt                            # Python dependencies
├── .gitignore                                  # Git ignore rules
└── README.md                                   # This file
```

---

## Contents

- **data/milestone1_real/**:  
  - `students_batch_XX_100K_cleaned.zip` – Ten cleaned batch archives (each contains a CSV)
  - `students_batch_XX_100K_cleaned.parquet` – **NEW!** Parquet versions (95% smaller, faster loading)
  - `cleaned_students.csv` – Full assembled dataset (generated locally from ZIP parts)
  - `cleaned_students.parquet` – **NEW!** Full assembled dataset in Parquet format
  - `sample_100K_students.zip` – Random sample of 100K students (ZIP)
  - `sample_100K_students.parquet` – **NEW!** Random sample in Parquet format
  - `summary_1M_real_data.csv` – Data summary and statistics

- **scripts/real_data_milestone1.py**:  
  - Script to generate the original dataset using real IPEDS data

- **scripts/clean_students_batches.py**:  
  - Script to clean each 100K batch, standardize fields, and produce `cleaned_students.csv`

- **scripts/create_sample_dataset.py**:  
  - Script to create a 100K-student sample by sampling from batches

- **scripts/verify_sample.py**:  
  - Script to verify row counts, distributions, and basic stats on the sample

- **scripts/assemble_dataset.py**:  
  - **UPDATED!** Now assembles Parquet files into `cleaned_students.parquet` (original CSV functionality preserved in comments)

- **scripts/convert_to_parquet.py**:  
  - **NEW!** Converts all CSV files to Parquet format while preserving originals

- **scripts/Milestone2_3_SQL_and_Visualizations.ipynb**:  
  - **MILESTONES 2 & 3 (COMPLETE)** Combined SQL analytics and visualization notebook
  - Star schema design and ETL pipeline
  - Advanced analytical queries and visualizations
  - ER diagram creation and performance analysis
  - Complete ETL pipeline processing 10M+ records
  - Four comprehensive visualizations (matplotlib, seaborn)
  - CSV export functionality

- **output/**:  
  - Generated analytical outputs and query results
  - Exported CSV files from SQL analyses:
    - `subject_performance_analysis.csv` - Average scores and attendance by subject
    - `top_performers.csv` - Top 100 performing students
    - `performance_by_university_type.csv` - Performance metrics by university type
    - `seasonal_performance_patterns.csv` - Performance trends by semester and month

- **docs/**:  
  - Project proposal and documentation
  - **data_dictionary.md**: Complete data dictionary with all 16 columns, data types, and valid ranges
  - Additional project-related PDFs and markdown files

- **assets/**:  
  - ER diagrams and database design visuals
  - Project timeline/Gantt charts
  - UI/UX wireframes and design mockups

- **dashboard/**:  
  - **app.py**: Working Streamlit dashboard with interactive visualizations
  - edu-analytics-dashboard.tsx: React/TypeScript prototype (not currently used)

- **requirements.txt**:  
  - Dependencies for Milestones 1 & 2 (includes pyarrow, duckdb, matplotlib, seaborn)

- **.gitignore**:  
  - Ignores large CSVs, Python cache, database files, and system files

---

## How to Use

1. **Install requirements**  
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Convert CSV files to Parquet format (recommended for better performance)**  
   
   ```bash
   python scripts/convert_to_parquet.py
   ```
   - Converts all CSV files to Parquet format (95% compression!)
   - Preserves original CSV files
   - Creates `.parquet` versions alongside existing files

3. **Assemble the full dataset from Parquet files**  
   
   ```bash
   python scripts/assemble_dataset.py
   ```
   - Discovers `students_batch_01..10_100K_cleaned.parquet`
   - Concatenates Parquet files in order
   - Writes `data/milestone1_real/cleaned_students.parquet`
   - Optional sample creation:
     
     ```bash
     python scripts/assemble_dataset.py --create-sample --rows-per-batch 10000
     ```

4. **Build the DuckDB database**  
   
   ```bash
   python scripts/build_database.py
   ```
   - Creates star schema database (820MB)
   - Builds 5 tables: 4 dimensions + 1 fact table
   - Processes 10M+ records in seconds
   - Generates `scripts/student_performance.duckdb`

5. **Launch the interactive dashboard**  
   
   ```bash
   python -m streamlit run dashboard/app.py
   ```
   - Opens at http://localhost:8501
   - Real-time querying from DuckDB
   - Interactive filters and visualizations

6. **Explore the data**  
   - Run the Jupyter notebook: `jupyter notebook "scripts/Milestone2_3_SQL_and_Visualizations.ipynb"`
   - Use the cleaned batch files for analysis, or `cleaned_students.parquet` for full-scale processing
   - See `summary_1M_real_data.csv` for quick stats
   - Check `output/` folder for exported query results
   - **Parquet files load 10-50x faster than CSV for large datasets!**

---

### **Advanced/Optional Steps**

**Convert CSV files to Parquet format:**  
```bash
python scripts/convert_to_parquet.py
```
- Converts all CSV files to Parquet format (95% compression!)
- Preserves original CSV files

**Regenerate the raw dataset from scratch:**  
```bash
python scripts/real_data_milestone1.py
```
> *Generates 10×100K batch CSVs from IPEDS inputs.*

**Clean the dataset in batches:**  
```bash
python scripts/clean_students_batches.py
```
- Processes batches 1–10 individually
- Writes `students_batch_XX_100K_cleaned.csv`

---

## Milestone 2: SQL Integration & Analytics 🎯

### **SQL Analytics Implementation (Complete)**

**Status**: ✅ **Complete** - All functionality implemented and tested

**Run the Milestone 2 analysis:**

```bash
# Open the Jupyter notebook
jupyter notebook "scripts/Milestone2_3_SQL_and_Visualizations.ipynb"
```

**Prerequisites:**
- Ensure `data/milestone1_real/cleaned_students.parquet` exists (run `python scripts/assemble_dataset.py` if needed)
- All dependencies installed: `pip install -r requirements.txt`

**What you'll get:**

1. **🏗️ Star Schema Database**
   - Professional-grade dimensional modeling
   - 5 tables: `dim_student`, `dim_university`, `dim_course`, `dim_date`, `fact_student_performance`
   - Optimized for analytical queries

2. **⚡ DuckDB Performance**
   - Direct Parquet integration (no import needed!)
   - 10-50x faster than traditional SQLite
   - ETL pipeline completes in seconds

3. **📊 Advanced Analytics**
   - Top performers by subject
   - Attendance trends over time
   - Score-attendance correlation analysis
   - Performance by university type
   - Seasonal performance patterns

4. **📈 Visualizations**
   - Subject performance bar charts
   - University type distribution
   - Attendance trends over time
   - Score distribution histograms

5. **🗺️ ER Diagram**
   - Visual representation of star schema
   - Professional database design documentation
   
   ![Entity Relationship Diagram](assets/ERD%20(Entity%20Relationship%20Diagram)%20based%20on%20the%20database%20design.png)
   
   *The Entity Relationship Diagram (ERD) above illustrates our star schema design, showing the relationships between dimension tables (`dim_student`, `dim_university`, `dim_course`, `dim_date`) and the central fact table (`fact_student_performance`). This design optimizes analytical queries by separating descriptive attributes from measurable facts.*

6. **📁 Exported Results**
   - `subject_performance_analysis.csv` - Comprehensive subject performance metrics
   - `top_performers.csv` - Top 100 students with highest scores
   - `performance_by_university_type.csv` - University type analysis
   - `seasonal_performance_patterns.csv` - Time-based performance trends

### **Key Insights Discovered:**
- **Foreign Language** has highest average scores (84.6)
- **Engineering subjects** show lower attendance (82%)
- **Strong correlation** between attendance and performance
- **Ivy League universities** show consistent high performance
- **Spring semester** shows slightly better attendance

### **Performance Metrics:**
- **Database Size**: 10M+ records across 5 tables
- **ETL Time**: < 5 seconds for complete pipeline
- **Query Performance**: Sub-second response for complex analytics
- **Storage Efficiency**: 95% compression with Parquet format

---

## Why Parquet? 🚀

We've added Parquet format support for significant performance improvements:

### **Storage Benefits**
- **95.4% compression**: 1.6GB → 75MB (20x smaller!)
- **Columnar storage**: Only read the columns you need
- **Built-in compression**: Automatic optimization for your data types

### **Performance Benefits**
- **10-50x faster loading**: Especially for large datasets
- **Faster queries**: Columnar access means better analytics
- **Type preservation**: Numbers stay numbers, dates stay dates
- **Schema embedded**: No guessing about data types

### **Example Performance Comparison**
```python
# CSV: Must load everything
df = pd.read_csv('cleaned_students.csv')  # ~30 seconds, 1.6GB
scores = df['score']  # Already loaded everything

# Parquet: Load only what you need
df = pd.read_parquet('cleaned_students.parquet', columns=['score'])  # ~2 seconds, 75MB
```

### **Backward Compatibility**
- Original CSV files are preserved
- Original CSV functionality is commented out in `assemble_dataset.py`
- Easy to switch back by uncommenting the CSV functions

---

## Sample Dataset (100K Students)

For development and testing, use the curated sample included (small enough to commit):

- `data/milestone1_real/sample_100K_students.csv`  
  - Built by sampling 10K random students from each cleaned batch (1–10) and including all their records
  - Reproducible sampling with a fixed seed

Create or refresh the sample:

```
python scripts/create_sample_dataset.py
```

Verify the sample statistics:

```
python scripts/verify_sample.py
```

Compressed version for GitHub uploads:

```
Compress-Archive -Path data/milestone1_real/sample_100K_students.csv -DestinationPath data/milestone1_real/sample_100K_students.zip -Force
```

---

## Data Details

For complete data dictionary including all column definitions, data types, and valid ranges, see **[docs/data_dictionary.md](docs/data_dictionary.md)**.

**Quick Overview:**

- **Students**: 1,000,000 unique
- **Universities**: 50 (see script for full list)
- **Subjects**: 31
- **Years**: 2010–2024
- **Records**: 9,999,795
- **Performance Categories**: Excellent, High, Medium, Low, Poor
- **Cleaning Standardization (scripts/clean_students_batches.py)**:
  - Anonymize names of form `Unk_Student_*` to `Student_00001` style
  - Map `university` → `state` (fallback to Unknown if unmapped)
  - Map `university` → `university_type` (Ivy League, Public, Private)
  - Rename `attendance` → `attendance_flag` and coerce to boolean
  - Normalize performance to: Low, Medium, High, Excellent, Poor
  - ISO dates (YYYY-MM-DD)
  - Final column order and snake_case consistency

---

## Validation (Quick Checks)

- Row counts by file (PowerShell):
```powershell
  Get-ChildItem "data/milestone1_real/*_cleaned.csv" | ForEach-Object { "$( $_.Name ): $( (Get-Content $_.FullName | Measure-Object -Line).Lines )" }
  ```

- Python sanity checks:
  
  ```python
  import pandas as pd
  df = pd.read_csv('data/milestone1_real/cleaned_students.csv')
  print('rows:', len(df), 'cols:', len(df.columns))
  print(df['performance_category'].value_counts())
  print(df['attendance_flag'].value_counts())
  print(df['state'].value_counts().head(10))
  print(pd.to_datetime(df['date'], errors='coerce').notna().mean())
  ```

- Spot-check columns are present and ordered:
  
  ```python
  expected = [
      'student_id','student_name','university','state','university_type','subject','score','grade','attendance_flag','performance_category','year','semester','date','credits','course_level','batch_number'
  ]
  df = pd.read_csv('data/milestone1_real/students_batch_01_100K_cleaned.csv', nrows=0)
  print(list(df.columns))
  ```

---

## Repository Hygiene

- The `.gitignore` excludes large raw/cleaned CSVs and batch files, but allows:
  - `data/milestone1_real/sample_100K_students.zip` (use ZIP for GitHub)
  - `data/milestone1_real/summary_1M_real_data.csv`

- If you plan to use Google Drive, ensure `gdown` is available (either via `requirements.txt` or manual install).

---

## What We Did (Changelog)

### **Milestone 1 (Original)**
- Implemented batch cleaning pipeline to process 10×100K CSVs with pandas
- Generated cleaned batch files: `students_batch_01_100K_cleaned.csv` … `students_batch_10_100K_cleaned.csv`
- Created combined cleaned dataset: `cleaned_students.csv`
- Deleted the old combined raw CSV to save space; retained cleaned batches
- Updated README with instructions, validation steps, and project structure

### **Parquet Enhancement (Latest)**
- **Added Parquet format support**: 95.4% compression (1.6GB → 75MB)
- **Created `convert_to_parquet.py`**: Converts all CSV files to Parquet while preserving originals
- **Updated `assemble_dataset.py`**: Now works with Parquet files (CSV functionality preserved in comments)
- **Performance boost**: 10-50x faster loading for large datasets
- **Backward compatibility**: All original CSV files and functionality preserved
- **Updated documentation**: Added Parquet benefits and usage instructions

### **Milestone 2: SQL Integration & Analytics (Complete)**
- **SQL analytics implementation**: Professional star schema database design
- **DuckDB integration**: Direct Parquet querying with 10-50x performance improvement
- **Complete ETL pipeline**: Processes 10M+ records in seconds
- **Advanced analytical queries**: 
  - Top performers by subject
  - Attendance trends over time
  - Score-attendance correlation analysis
  - Performance by university type
  - Seasonal performance patterns
- **Comprehensive visualizations**: Four chart types (bar, pie, line, histogram)
- **ER diagram generation**: Programmatic star schema visualization
- **Export functionality**: Four CSV exports with comprehensive analytics
- **Performance optimization**: Sub-second query response for 10M+ records
- **Status**: ✅ Complete and production-ready

### **Project Structure Improvements**
- **Reorganized project structure**: Added `docs/`, `assets/`, and `dashboard/` directories
- **Better file organization**: Separated documentation, visuals, and UI components
- **Removed duplicates**: Cleaned up duplicate files and empty directories
- **Added .gitignore**: Comprehensive ignore rules for data files, databases, and system files

---

## Project Timeline & Planning 📅

Our project follows a structured four-milestone approach to deliver a comprehensive student performance dashboard. The timeline below outlines key deliverables, deadlines, and dependencies across all milestones.

![Project Timeline Gantt Chart](assets/TimelineGantt%20chart%20for%20the%20project%20plan.png)

*The Gantt chart above provides a visual overview of our project timeline, showing milestone deadlines, key deliverables, and the sequential progression from data preprocessing through to final documentation. This helps coordinate team efforts and ensures timely completion of each phase.*

### **Milestone Overview:**
- **Milestone 1** (Oct 31, 2025) ✅ **Complete**: Data preprocessing, cleaning, and Parquet optimization
- **Milestone 2** (Nov 7, 2025) ✅ **Complete**: SQL integration, star schema database, and advanced analytics
- **Milestone 3** (Nov 20, 2025) ✅ **Complete**: Visualization and interactive dashboard development
- **Milestone 4** (Dec 1, 2025) 📋 **Planned**: Final documentation, report, and presentation

---

## UI/UX Design & Dashboard Wireframes 🎨

The dashboard design prioritizes clarity, accessibility, and actionable insights for teachers and administrators. Our wireframes illustrate the user flow from high-level overview to detailed student analysis.

![Dashboard Wireframes](assets/wireframes%20for%20the%20UIUX%20design.png)

*The wireframes above showcase our dashboard design, featuring:*
- **Overview Dashboard**: Key performance indicators (KPIs), quick filters by cohort/subject/time range, and summary statistics
- **Student Profile View**: Detailed individual student performance timeline, attendance log, and performance category breakdown
- **Cohort Trend Analysis**: Comparative analysis with trend charts and heatmaps for subject performance distribution

### **Design Principles:**
- **Accessibility**: High-contrast color palette that is color-blind friendly
- **Usability**: Clear labels and intuitive navigation for both technical and non-technical users
- **Actionability**: Complex data presented with simple, actionable interpretations

---

## Next Steps for the Team

### **✅ Milestone 2: SQL Integration & Querying - COMPLETE**
- **Goal**: Store the cleaned data in a SQL database and practice advanced querying.
- **Status**: ✅ **COMPLETE** - All objectives achieved and tested
- **Achievements**:
  1. ✅ Designed normalized star schema (Students, Universities, Courses, Dates, Performance)
  2. ✅ Implemented complete ETL pipeline with DuckDB (10-50x faster than SQLite)
  3. ✅ Wrote advanced SQL queries for:
     - ✅ Top performers by subject
     - ✅ Attendance trends over time
     - ✅ Average scores by subject
     - ✅ Score-attendance correlation analysis
     - ✅ Performance by university type
     - ✅ Seasonal performance patterns
  4. ✅ Documented schema and queries with programmatic ER diagram
  5. ✅ Created four comprehensive visualizations
  6. ✅ Exported all analytical results to CSV
- **Deliverables Completed**:
  - ✅ ER diagram (programmatically generated in notebook)
  - ✅ Complete ETL pipeline (staging → dimensions → fact table)
  - ✅ All query results exported to CSV files (4 files)
  - ✅ Performance analysis and optimization
  - ✅ Four comprehensive visualizations (bar, pie, line, histogram)
  - ✅ Database statistics and validation

---

 
### **✅ Milestone 3: Visualization & Reporting - COMPLETE**
- **Goal**: Use Python to visualize student performance over time.
- **Status**: ✅ **COMPLETE** - All objectives achieved
- **Deliverables Completed**:
  - ✅ Python notebook with visualizations: `Milestone2_3_SQL_and_Visualizations.ipynb`
  - ✅ Interactive Streamlit dashboard: `dashboard/app.py`
  - ✅ Attendance heatmaps (Plotly in dashboard)
  - ✅ Score trends and distribution charts

**Run the dashboard:**
```bash
python -m streamlit run dashboard/app.py
```

**Note:** Milestone 3 visualization requirements are fulfilled through both the interactive dashboard AND the visualizations in the Milestone 2 & 3 combined notebook.

---

 
### **Milestone 4: Final Documentation and Presentation**
- **Goal**: Summarize findings and show visual outputs.
- **Tasks**:
  1. Document:
     - Key patterns in student performance
     - How the dashboard helps teachers or school admins
  2. Present:
     - The visual report and live dashboard (if built)
- **Deliverables**:
  - Final Report PDF
  ️- Presentation Slides

---

 
## License

This project is for educational and research purposes.  
Data is generated using public IPEDS sources and synthetic student records.

---

**🎉 Milestones 1, 2 & 3 Complete - Ready for Milestone 4: Final Documentation!**

## 🏆 Project Status Summary

| Milestone | Status | Key Achievements |
|-----------|--------|------------------|
| **Milestone 1** | ✅ Complete | 1M student dataset, Parquet optimization, 95% compression |
| **Milestone 2** | ✅ Complete | Star schema, DuckDB analytics, advanced SQL queries, visualizations, ER diagram |
| **Milestone 3** | ✅ Complete | Interactive Streamlit dashboard, attendance heatmaps, visualizations |
| **Milestone 4** | 📋 Planned | Final documentation and presentation |

**Milestones 1-3 complete! Ready for Milestone 4: Final Documentation and Presentation.**

## Quick Start Guide

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Data Project"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the dataset** (if not already done)
   ```bash
   python scripts/assemble_dataset.py
   ```

4. **Run Milestone 2 & 3 analysis**
   ```bash
   jupyter notebook "scripts/Milestone2_3_SQL_and_Visualizations.ipynb"
   ```
   Or on Windows PowerShell:
   ```powershell
   jupyter notebook "scripts\Milestone2_3_SQL_and_Visualizations.ipynb"
   ```

5. **Launch the interactive dashboard**
   ```bash
   python -m streamlit run dashboard/app.py
   ```

6. **View results**
   - Check `output/` folder for exported CSV files
   - Review visualizations in the notebook
   - Examine ER diagram in the notebook
   - Explore the interactive dashboard at http://localhost:8501

## Repository Structure for GitHub

This repository is organized for easy navigation and GitHub compatibility:

- **Data files**: Parquet format for efficient storage (95% compression)
- **Scripts**: All Python scripts and Jupyter notebooks in `scripts/` folder
- **Output**: Generated CSV files (excluded from git via `.gitignore`)
- **Documentation**: README, proposals, and guides in `docs/` folder
- **Assets**: Visual diagrams and wireframes in `assets/` folder

### Important Notes for GitHub:
- Large data files (CSV, database files) are excluded via `.gitignore`
- Parquet files are included for efficient data sharing
- Sample dataset (`sample_100K_students.parquet`) is included for testing
- All output files are generated by running the notebook
