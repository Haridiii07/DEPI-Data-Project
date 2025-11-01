"""
Convert CSV files to Parquet format while preserving originals.

This script converts all CSV files in data/milestone1_real/ to Parquet format,
keeping the original CSV files intact. Parquet files will be created with
the same base name but .parquet extension.

Usage (from project root):
  python scripts/convert_to_parquet.py

Dependencies: pandas, pyarrow
"""

import os
import glob
from pathlib import Path
import pandas as pd


def convert_csv_to_parquet(csv_path: str) -> str:
    """Convert a single CSV file to Parquet format."""
    csv_file = Path(csv_path)
    parquet_path = csv_file.with_suffix('.parquet')
    
    print(f"Converting: {csv_file.name} -> {parquet_path.name}")
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Write Parquet
    df.to_parquet(parquet_path, index=False)
    
    # Show file size comparison
    csv_size = csv_file.stat().st_size
    parquet_size = parquet_path.stat().st_size
    compression_ratio = (1 - parquet_size / csv_size) * 100
    
    print(f"  CSV size: {csv_size:,} bytes")
    print(f"  Parquet size: {parquet_size:,} bytes")
    print(f"  Compression: {compression_ratio:.1f}% reduction")
    print()
    
    return str(parquet_path)


def main():
    """Convert all CSV files in data/milestone1_real/ to Parquet."""
    data_dir = Path("data/milestone1_real")
    
    if not data_dir.exists():
        print(f"Error: Directory {data_dir} does not exist")
        return
    
    # Find all CSV files
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files to convert:")
    print()
    
    converted_files = []
    total_csv_size = 0
    total_parquet_size = 0
    
    for csv_file in sorted(csv_files):
        parquet_path = convert_csv_to_parquet(csv_file)
        converted_files.append(parquet_path)
        
        # Track total sizes
        total_csv_size += csv_file.stat().st_size
        total_parquet_size += Path(parquet_path).stat().st_size
    
    print("=" * 50)
    print("CONVERSION SUMMARY")
    print("=" * 50)
    print(f"Files converted: {len(converted_files)}")
    print(f"Total CSV size: {total_csv_size:,} bytes ({total_csv_size / 1024 / 1024:.1f} MB)")
    print(f"Total Parquet size: {total_parquet_size:,} bytes ({total_parquet_size / 1024 / 1024:.1f} MB)")
    print(f"Overall compression: {(1 - total_parquet_size / total_csv_size) * 100:.1f}% reduction")
    print()
    print("Converted files:")
    for parquet_file in converted_files:
        print(f"  - {Path(parquet_file).name}")


if __name__ == "__main__":
    main()
