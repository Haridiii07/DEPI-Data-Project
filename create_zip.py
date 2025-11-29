import zipfile
import os

def zip_project(output_filename):
    # Files/Dirs to include
    include_dirs = ['src', 'docs', 'notebooks', '.github', 'assets']
    include_files = ['README.md', 'requirements.txt', 'pyproject.toml']
    
    # Data files to include (only small ones)
    include_data = [
        'data/sample_50K_students.parquet',
        'data/star_schema/dim_course.parquet',
        'data/star_schema/dim_date.parquet',
        'data/star_schema/dim_university.parquet'
    ]

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add root files
        for f in include_files:
            if os.path.exists(f):
                zipf.write(f, f)
        
        # Add directories
        for d in include_dirs:
            for root, dirs, files in os.walk(d):
                # Skip __pycache__
                if '__pycache__' in root:
                    continue
                    
                for file in files:
                    if file == '.DS_Store' or file.endswith('.pyc'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)
        
        # Add specific data files
        for f in include_data:
            if os.path.exists(f):
                zipf.write(f, f)
                
    print(f"✅ Created {output_filename}")

if __name__ == "__main__":
    os.makedirs("submission", exist_ok=True)
    zip_project("submission/Project_Source_Code.zip")
