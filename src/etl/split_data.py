import os
from pathlib import Path
import math

def split_file(file_path, chunk_size_mb=45):
    """
    Splits a large file into smaller chunks.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    file_size = file_path.stat().st_size
    chunk_size = chunk_size_mb * 1024 * 1024
    num_chunks = math.ceil(file_size / chunk_size)

    print(f"📦 Splitting {file_path.name} ({file_size / (1024*1024):.2f} MB) into {num_chunks} chunks...")

    with open(file_path, 'rb') as f:
        for i in range(num_chunks):
            chunk_data = f.read(chunk_size)
            chunk_name = f"{file_path.name}.part{i+1}"
            chunk_path = file_path.parent / chunk_name
            
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk_data)
            
            print(f"   - Created {chunk_name} ({len(chunk_data) / (1024*1024):.2f} MB)")

    print("✅ Split complete.")

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent.parent
    target_file = base_dir / 'data' / 'cleaned_students.parquet'
    split_file(target_file)
