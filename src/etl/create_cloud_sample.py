import pandas as pd
from pathlib import Path

def create_cloud_sample():
    """Create a 200K sample for Streamlit Cloud deployment."""
    base_dir = Path(__file__).parent.parent.parent
    source_file = base_dir / 'data' / 'cleaned_students.parquet'
    output_file = base_dir / 'data' / 'sample_200K_students.parquet'
    
    print(f"📂 Loading data from {source_file}...")
    df = pd.read_parquet(source_file)
    
    print(f"📊 Total records: {len(df):,}")
    
    # Sample 200K records (20% of 1M)
    sample_size = 200_000
    print(f"🎯 Creating sample of {sample_size:,} records...")
    
    # Use random sampling with a fixed seed for reproducibility
    sample_df = df.sample(n=sample_size, random_state=42)
    
    print(f"💾 Saving to {output_file}...")
    sample_df.to_parquet(output_file, index=False)
    
    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f"✅ Sample created: {len(sample_df):,} records, {file_size:.2f} MB")

if __name__ == "__main__":
    create_cloud_sample()
