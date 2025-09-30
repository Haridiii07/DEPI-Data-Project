#!/usr/bin/env python3
"""
Create a random sample dataset of 100K students from the cleaned batch files.

This script:
1. Reads each of the 10 batch files (students_batch_XX_100K_cleaned.csv)
2. Randomly samples 10K students from each batch
3. Combines them into a single sample file with 100K students
4. Saves as 'sample_100K_students.csv' in the data/milestone1_real/ directory
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def create_sample_dataset():
    """Create a random sample of 100K students from batch files."""
    
    # Set up paths
    data_dir = Path("data/milestone1_real")
    output_file = data_dir / "sample_100K_students.csv"
    
    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    print("Creating random sample dataset of 100K students...")
    print("=" * 60)
    
    all_samples = []
    total_students = 0
    
    # Process each batch file (1-10)
    for batch_num in range(1, 11):
        batch_file = data_dir / f"students_batch_{batch_num:02d}_100K_cleaned.csv"
        
        if not batch_file.exists():
            print(f"Warning: {batch_file.name} not found, skipping...")
            continue
            
        print(f"Processing {batch_file.name}...")
        
        try:
            # Read the batch file
            df_batch = pd.read_csv(batch_file)
            print(f"   Loaded {len(df_batch):,} records")
            
            # Get unique students in this batch
            unique_students = df_batch['student_id'].unique()
            print(f"   Found {len(unique_students):,} unique students")
            
            # Sample 10K students (or all if less than 10K)
            sample_size = min(10000, len(unique_students))
            sampled_student_ids = np.random.choice(unique_students, size=sample_size, replace=False)
            
            print(f"   Randomly sampling {sample_size:,} students...")
            
            # Get all records for the sampled students
            df_sample = df_batch[df_batch['student_id'].isin(sampled_student_ids)]
            
            print(f"   Sampled {len(df_sample):,} records for {sample_size:,} students")
            
            all_samples.append(df_sample)
            total_students += sample_size
            
        except Exception as e:
            print(f"   Error processing {batch_file.name}: {e}")
            continue
    
    if not all_samples:
        print("No batch files were processed successfully!")
        return
    
    # Combine all samples
    print("\nCombining all samples...")
    df_combined = pd.concat(all_samples, ignore_index=True)
    
    print(f"Final dataset statistics:")
    print(f"   Total records: {len(df_combined):,}")
    print(f"   Unique students: {df_combined['student_id'].nunique():,}")
    print(f"   Universities: {df_combined['university'].nunique()}")
    print(f"   Subjects: {df_combined['subject'].nunique()}")
    print(f"   Years: {df_combined['year'].min()} - {df_combined['year'].max()}")
    
    # Save the sample dataset
    print(f"\nSaving sample dataset to {output_file}...")
    df_combined.to_csv(output_file, index=False)
    
    # Verify the saved file
    file_size = output_file.stat().st_size / (1024 * 1024)  # Size in MB
    print(f"Sample dataset saved successfully!")
    print(f"   File: {output_file}")
    print(f"   Size: {file_size:.2f} MB")
    print(f"   Records: {len(df_combined):,}")
    print(f"   Students: {df_combined['student_id'].nunique():,}")
    
    # Show sample of the data
    print(f"\nSample data preview:")
    print(df_combined.head())
    
    print(f"\nSample dataset creation completed!")
    print(f"   You can now upload 'sample_100K_students.csv' to your repository.")

if __name__ == "__main__":
    create_sample_dataset()
