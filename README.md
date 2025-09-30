# Student Performance Data Project – Milestone 1

## Overview

This repository contains the **Milestone 1** deliverable for the Student Performance Dashboard project.  
It provides a fully preprocessed, large-scale dataset of **1 million students** from the **top 50 U.S. universities** (2010–2024), generated using real IPEDS institutional data and robust data science best practices.

## Table of Contents

- [Folder Structure](#folder-structure)
- [Contents](#contents)
- [How to Use](#how-to-use)
- [Dataset Access (Google Drive)](#dataset-access-google-drive)
- [Sample Dataset (100K Students)](#sample-dataset-100k-students)
- [Data Details](#data-details)
- [Validation (Quick Checks)](#validation-quick-checks)
- [What We Did (Changelog)](#what-we-did-changelog)
- [Next Steps for the Team](#next-steps-for-the-team)
- [License](#license)

---

## Folder Structure

```
Data Project/
├── data/
│   └── milestone1_real/
│       ├── cleaned_students.csv                # Full cleaned dataset (downloaded via Drive)
│       ├── students_batch_01_100K_cleaned.csv
│       ├── ... (up to students_batch_10_100K_cleaned.csv)
│       ├── sample_100K_students.csv            # Random sample (10K per batch, 100K students total) [not pushed]
│       └── summary_1M_real_data.csv
├── scripts/
│   ├── real_data_milestone1.py
│   ├── clean_students_batches.py
│   ├── create_sample_dataset.py                # Creates 100K-student sample from batches
│   └── verify_sample.py                        # Verifies sample dataset stats
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Contents

- **data/milestone1_real/**:  
  - `cleaned_students.csv` – Full cleaned dataset (concatenated from cleaned batches)
  - `students_batch_XX_100K_cleaned.csv` – 10 device-friendly cleaned batch files
  - `sample_100K_students.csv` – Random sample of 100K students (10K per batch)
  - `summary_1M_real_data.csv` – Data summary and statistics

- **scripts/real_data_milestone1.py**:  
  - Script to generate the original dataset using real IPEDS data

- **scripts/clean_students_batches.py**:  
  - Script to clean each 100K batch, standardize fields, and produce `cleaned_students.csv`

- **scripts/create_sample_dataset.py**:  
  - Script to create `sample_100K_students.csv` by sampling 10K students from each batch

- **scripts/verify_sample.py**:  
  - Script to verify row counts, distributions, and basic stats on the sample

- **requirements.txt**:  
  - Minimal dependencies for Milestone 1

- **.gitignore**:  
  - Ignores large CSVs, Python cache, and system files

---

## How to Use

1. **Install requirements**  
   ```
   pip install -r requirements.txt
   ```

2. **(Optional) Regenerate the raw dataset**  
   ```
   python scripts/real_data_milestone1.py
   ```
   > *Generates 10×100K batch CSVs and a combined CSV from IPEDS inputs.*

3. **Clean the dataset in batches (recommended for 1M data)**  
   ```
   python scripts/clean_students_batches.py
   ```
   - Processes batches 1–10 individually to limit memory usage
   - Writes `students_batch_XX_100K_cleaned.csv`
   - Concatenates them into `cleaned_students.csv`
   - Removes the old combined raw file if present

4. **Explore the data**  
   - Use the cleaned batch files for analysis, or `cleaned_students.csv` for full-scale processing.
   - See `summary_1M_real_data.csv` for quick stats.

---

## Dataset Access (Google Drive)

The full dataset (~3 GB) is hosted on Google Drive due to size constraints. Download it locally using `gdown`:

1. Install tools (if not already installed):
   ```
   pip install gdown pandas
   ```

2. Download the full dataset:
   ```python
   import gdown, os

   os.makedirs("data/milestone1_real", exist_ok=True)
   file_id = "YOUR_FILE_ID"  # Replace with the actual Google Drive file ID
   url = f"https://drive.google.com/uc?id={file_id}"
   output = "data/milestone1_real/cleaned_students.csv"
   gdown.download(url, output, quiet=False)
   print("Dataset downloaded to:", output)
   ```

3. Quick verification:
   ```python
   import pandas as pd, os
   f = "data/milestone1_real/cleaned_students.csv"
   print("Exists:", os.path.exists(f), "Size (GB):", os.path.getsize(f)/(1024**3))
   print(pd.read_csv(f, nrows=5))
   ```

> Note: Do not commit the full dataset to Git. Use the sample file for the repo.

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
  ```
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

- Implemented batch cleaning pipeline to process 10×100K CSVs with pandas
- Generated cleaned batch files: `students_batch_01_100K_cleaned.csv` … `students_batch_10_100K_cleaned.csv`
- Created combined cleaned dataset: `cleaned_students.csv`
- Deleted the old combined raw CSV to save space; retained cleaned batches
- Updated README with instructions, validation steps, and project structure

---

## Next Steps for the Team

### **Milestone 2: SQL Integration & Querying**
- **Goal**: Store the cleaned data in a SQL database and practice advanced querying.
- **Tasks**:
  1. Design a normalized relational schema (e.g., Students, Subjects, Scores).
  2. Import the cleaned data into SQLite or PostgreSQL using Python.
  3. Write SQL queries to:
     - Get top performers by subject
     - Analyze attendance trends
     - Calculate average scores by month
  4. Document the schema and queries.
- **Deliverables**:
  - ER diagram
  - SQL scripts for table creation and queries
  - Query result screenshots or exported data

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

**Ready for team collaboration and further development!**
