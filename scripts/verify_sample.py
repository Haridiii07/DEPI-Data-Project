#!/usr/bin/env python3
"""
Verify the sample dataset created by create_sample_dataset.py
"""

import pandas as pd
from pathlib import Path

def verify_sample_dataset():
    """Verify the sample dataset statistics."""
    
    sample_file = Path("data/milestone1_real/sample_100K_students.csv")
    
    if not sample_file.exists():
        print("Error: Sample dataset file not found!")
        return
    
    print("Verifying sample dataset...")
    print("=" * 50)
    
    # Load the sample dataset
    df = pd.read_csv(sample_file)
    
    print(f"Dataset Overview:")
    print(f"  Total records: {len(df):,}")
    print(f"  Unique students: {df['student_id'].nunique():,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  File size: {sample_file.stat().st_size / (1024*1024):.2f} MB")
    
    print(f"\nData Distribution:")
    print(f"  Universities: {df['university'].nunique()}")
    print(f"  Subjects: {df['subject'].nunique()}")
    print(f"  Years: {df['year'].min()} - {df['year'].max()}")
    print(f"  University types: {df['university_type'].nunique()}")
    
    print(f"\nPerformance Categories:")
    perf_counts = df['performance_category'].value_counts()
    for category, count in perf_counts.items():
        print(f"  {category}: {count:,} ({count/len(df)*100:.1f}%)")
    
    print(f"\nAttendance:")
    attendance_counts = df['attendance_flag'].value_counts()
    for flag, count in attendance_counts.items():
        print(f"  {flag}: {count:,} ({count/len(df)*100:.1f}%)")
    
    print(f"\nTop 5 Universities by Record Count:")
    uni_counts = df['university'].value_counts().head()
    for uni, count in uni_counts.items():
        print(f"  {uni}: {count:,}")
    
    print(f"\nTop 5 Subjects by Record Count:")
    subj_counts = df['subject'].value_counts().head()
    for subj, count in subj_counts.items():
        print(f"  {subj}: {count:,}")
    
    print(f"\nSample Data Preview:")
    print(df.head())
    
    print(f"\nColumn Information:")
    print(df.info())

if __name__ == "__main__":
    verify_sample_dataset()
