import pandas as pd
from pathlib import Path

def create_50k_students_sample():
    """Create a sample with the first 50K UNIQUE STUDENTS (not records)."""
    base_dir = Path(__file__).parent.parent.parent
    source_file = base_dir / 'data' / 'cleaned_students.parquet'
    output_file = base_dir / 'data' / 'sample_50K_students.parquet'
    
    print(f"📂 Loading data from {source_file}...")
    
    # Read the full file
    df = pd.read_parquet(source_file)
    
    print(f"📊 Total records: {len(df):,}")
    print(f"📊 Total unique students: {df['student_id'].nunique():,}")
    
    # Get first 50K unique students (in order they appear)
    unique_students = df['student_id'].unique()[:50_000]
    
    print(f"🎯 Selected first {len(unique_students):,} unique students")
    
    # Filter all records for these students
    sample_df = df[df['student_id'].isin(unique_students)].copy()
    
    # Create a mapping: student_id -> student_number (1-50,000)
    student_id_to_number = {student_id: i+1 for i, student_id in enumerate(unique_students)}
    sample_df['student_number'] = sample_df['student_id'].map(student_id_to_number)
    
    print(f"✅ Sample includes {len(unique_students):,} unique students")
    print(f"✅ Total records for these students: {len(sample_df):,}")
    print(f"✅ Average records per student: {len(sample_df)/len(unique_students):.1f}")
    
    print(f"💾 Saving to {output_file}...")
    sample_df.to_parquet(output_file, index=False, compression='snappy')
    
    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f"✅ Sample created: {file_size:.2f} MB")

if __name__ == "__main__":
    create_50k_students_sample()
