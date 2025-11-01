# Student Performance Data Project

## Overview

This repository contains **Milestone 1** and **Milestone 2** (in progress) deliverables for the Student Performance Dashboard project.  
It provides a fully preprocessed, large-scale dataset of **1 million students** from the **top 50 U.S. universities** (2010–2024), with advanced SQL analytics and star schema database implementation using DuckDB for optimal performance.

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
│   ├── DEPI_SQL Integration & Querying-Copy1 - Copy.ipynb  # Milestone 2: SQL Analytics
│   └── student_performance.duckdb              # DuckDB database file
├── output/
│   └── subject_performance.csv                # Generated analytical outputs
├── docs/                                       # Documentation and proposals
│   ├── Proposal_ Student Performance Dashboard.md
│   └── *.pdf                                   # Additional documentation PDFs
├── assets/                                     # Visual assets and diagrams
│   ├── ERD (Entity Relationship Diagram) based on the database design.png
│   ├── TimelineGantt chart for the project plan.png
│   └── wireframes for the UIUX design.png
├── dashboard/                                  # Dashboard UI components
│   └── edu-analytics-dashboard.tsx             # React dashboard component
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

- **scripts/DEPI_SQL Integration & Querying-Copy1 - Copy.ipynb**:  
  - **MILESTONE 2 (IN PROGRESS)** SQL analytics notebook with DuckDB implementation
  - Star schema design and ETL pipeline
  - Advanced analytical queries and visualizations
  - ER diagram creation and performance analysis

- **output/**:  
  - Generated analytical outputs and query results
  - Exported CSV files from SQL analyses

- **docs/**:  
  - Project proposal and documentation
  - Additional project-related PDFs and markdown files

- **assets/**:  
  - ER diagrams and database design visuals
  - Project timeline/Gantt charts
  - UI/UX wireframes and design mockups

- **dashboard/**:  
  - Dashboard UI components and frontend code
  - React/TypeScript dashboard implementation

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

3. **Assemble the full dataset from Parquet files (recommended)**  
   
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

4. **Alternative: Assemble from ZIP parts (legacy method)**  
   
   ```bash
   # Original CSV functionality is preserved in comments within assemble_dataset.py
   # Uncomment the CSV functions if you need to work with ZIP files
   ```

5. **(Optional) Regenerate the raw dataset**  
   
   ```bash
   python scripts/real_data_milestone1.py
   ```
   > *Generates 10×100K batch CSVs and a combined CSV from IPEDS inputs.*

6. **Clean the dataset in batches (if regenerating)**  
   
   ```bash
   python scripts/clean_students_batches.py
   ```
   - Processes batches 1–10 individually to limit memory usage
   - Writes `students_batch_XX_100K_cleaned.csv` then ZIPs
   - Concatenates them into `cleaned_students.csv` (or assemble later from ZIPs)
   - Removes the old combined raw file if present

7. **Explore the data**  
   - Use the cleaned batch files for analysis, or `cleaned_students.parquet` for full-scale processing.
   - See `summary_1M_real_data.csv` for quick stats.
   - **Parquet files load 10-50x faster than CSV for large datasets!**

---

## Milestone 2: SQL Integration & Analytics 🎯

### **SQL Analytics Implementation (Almost Complete)**

**Status**: 🚧 **In Progress** - Core functionality implemented, final refinements in progress

**Run the Milestone 2 analysis:**

```bash
# Open the Jupyter notebook
jupyter notebook "scripts/DEPI_SQL Integration & Querying-Copy1 - Copy.ipynb"
```

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
   - `subject_performance_analysis.csv`
   - `top_performers.csv`
   - `schema_creation.sql`
   - `analytical_queries.sql`

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

### **Milestone 2: SQL Integration & Analytics (In Progress)**
- **SQL analytics implementation**: Professional star schema database design
- **DuckDB integration**: Direct Parquet querying with 10-50x performance improvement
- **Advanced analytical queries**: Top performers, attendance trends, correlation analysis
- **Comprehensive visualizations**: Multiple chart types with insights
- **ER diagram creation**: Professional database design documentation
- **Export functionality**: SQL scripts and CSV results for analyses
- **Performance optimization**: Sub-second query response for 10M+ records
- **Status**: Core functionality complete, final refinements in progress

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
- **Milestone 2** (Nov 7, 2025) 🚧 **Almost Done**: SQL integration, star schema database, and advanced analytics
- **Milestone 3** (Nov 20, 2025) 🎯 **Next**: Visualization and interactive dashboard development
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

### **🚧 Milestone 2: SQL Integration & Querying - IN PROGRESS**
- **Goal**: Store the cleaned data in a SQL database and practice advanced querying.
- **Status**: 🚧 **ALMOST DONE** - Core objectives achieved, final refinements in progress
- **Achievements**:
  1. ✅ Designed normalized star schema (Students, Universities, Courses, Dates, Performance)
  2. ✅ Imported data into DuckDB with Python (10-50x faster than SQLite)
  3. ✅ Wrote advanced SQL queries for:
     - ✅ Top performers by subject
     - ✅ Attendance trends analysis
     - ✅ Average scores by month and subject
     - ✅ Performance correlation analysis
     - ✅ University type comparisons
  4. ✅ Documented schema and queries with ER diagram
- **Deliverables Completed**:
  - ✅ ER diagram (visualized in notebook)
  - ✅ SQL scripts for table creation and queries
  - ✅ Query results exported to CSV files
  - ✅ Performance analysis and optimization
  - ✅ Comprehensive visualizations

---

 
### **Milestone 3: Visualization & Reporting**
- **Goal**: Use Python to visualize student performance over time.
- **Tasks**:
  1. Use matplotlib or seaborn to show:
     - Score trends
     - Attendance heatmaps
  2. (Optional) Create an interactive dashboard using Streamlit or Plotly Dash.
- **Deliverables**:
  - Python notebook with visualizations
  - Simple dashboard (optional)

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

**🎉 Milestone 1 Complete - Milestone 2 Almost Done - Preparing for Milestone 3: Visualization & Reporting!**

## 🏆 Project Status Summary

| Milestone | Status | Key Achievements |
|-----------|--------|------------------|
| **Milestone 1** | ✅ Complete | 1M student dataset, Parquet optimization, 95% compression |
| **Milestone 2** | 🚧 Almost Done | Star schema, DuckDB analytics, advanced SQL queries (final refinements) |
| **Milestone 3** | 🎯 Next | Visualization & reporting dashboard |
| **Milestone 4** | 📋 Planned | Final documentation and presentation |

**Project structure improved and ready for final Milestone 2 completion and Milestone 3 development!**
