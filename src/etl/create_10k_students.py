import pandas as pd
from pathlib import Path

def create_10k_students_sample():
    """Create a sample with 10K RANDOM UNIQUE STUDENTS (not records)."""
    base_dir = Path(__file__).parent.parent.parent
    source_file = base_dir / 'data' / 'cleaned_students.parquet'
    output_file = base_dir / 'data' / 'sample_50K_students.parquet'  # Keep same name for cloud
    
    print(f"📂 Loading data from {source_file}...")
    
    # Read the full file
    df = pd.read_parquet(source_file)
    
    print(f"📊 Total records: {len(df):,}")
    print(f"📊 Total unique students: {df['student_id'].nunique():,}")
    
    # Get 10K RANDOM unique students
    all_students = df['student_id'].unique()
    selected_students = pd.Series(all_students).sample(n=10_000, random_state=42).tolist()
    
    print(f"🎯 Selected {len(selected_students):,} random unique students")
    
    # Filter all records for these students
    sample_df = df[df['student_id'].isin(selected_students)].copy()
    
    # Create a mapping: student_id -> student_number (1-10,000)
    # Sort by student_id to ensure consistent numbering
    selected_students_sorted = sorted(selected_students)
    student_id_to_number = {student_id: i+1 for i, student_id in enumerate(selected_students_sorted)}
    sample_df['student_number'] = sample_df['student_id'].map(student_id_to_number)
    
    print(f"✅ Sample includes {len(selected_students):,} unique students")
    print(f"✅ Total records for these students: {len(sample_df):,}")
    print(f"✅ Average records per student: {len(sample_df)/len(selected_students):.1f}")
    
    print(f"💾 Saving to {output_file}...")
    sample_df.to_parquet(output_file, index=False, compression='snappy')
    
    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f"✅ Sample created: {file_size:.2f} MB")

if __name__ == "__main__":
    create_10k_students_sample()
