"""
Basic import and function tests for Python scripts.
"""

import os
import sys
import pytest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestScriptImports:
    """Test that all scripts can be imported without errors."""
    
    def test_import_assemble_dataset(self):
        """Test assemble_dataset module can be imported."""
        import assemble_dataset
        assert hasattr(assemble_dataset, 'main')
        assert hasattr(assemble_dataset, 'assemble')
        assert hasattr(assemble_dataset, 'parse_args')
    
    def test_import_clean_students_batches(self):
        """Test clean_students_batches module can be imported."""
        import clean_students_batches
        assert hasattr(clean_students_batches, 'main')
    
    def test_import_convert_to_parquet(self):
        """Test convert_to_parquet module can be imported."""
        import convert_to_parquet
        assert hasattr(convert_to_parquet, 'main')
    
    def test_import_create_sample_dataset(self):
        """Test create_sample_dataset module can be imported."""
        import create_sample_dataset
        assert hasattr(create_sample_dataset, 'create_sample_dataset')
    
    def test_import_generate_summary(self):
        """Test generate_summary module can be imported."""
        import generate_summary
        assert hasattr(generate_summary, 'main')
    
    def test_import_verify_sample(self):
        """Test verify_sample module can be imported."""
        import verify_sample
        assert hasattr(verify_sample, 'verify_sample_dataset')


class TestScriptFunctions:
    """Test basic functionality of script functions."""
    
    def test_assemble_dataset_find_batch_files(self):
        """Test that assemble_dataset can find batch files."""
        import assemble_dataset
        batch_files = assemble_dataset.find_batch_parquet_files()
        # Should return a list (may be empty if no files exist)
        assert isinstance(batch_files, list)
    
    def test_assemble_dataset_parse_args(self):
        """Test that assemble_dataset argument parser works."""
        import assemble_dataset
        import argparse
        
        # Test default args
        sys.argv = ['assemble_dataset.py']
        args = assemble_dataset.parse_args()
        assert isinstance(args, argparse.Namespace)
        assert args.create_sample is False
        assert args.rows_per_batch == 10000
        assert args.random_seed == 7
    
    def test_batch_sort_key(self):
        """Test batch_sort_key function."""
        import assemble_dataset
        
        # Test valid batch file name
        path1 = "data/milestone1_real/students_batch_01_100K_cleaned.parquet"
        assert assemble_dataset.batch_sort_key(path1) == 1
        
        path2 = "data/milestone1_real/students_batch_10_100K_cleaned.parquet"
        assert assemble_dataset.batch_sort_key(path2) == 10
        
        # Test invalid path (should return 9999)
        path3 = "invalid_path.parquet"
        assert assemble_dataset.batch_sort_key(path3) == 9999


class TestScriptStructure:
    """Test that scripts have expected structure."""
    
    def test_scripts_directory_exists(self):
        """Test that scripts directory exists."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        assert scripts_dir.exists()
        assert scripts_dir.is_dir()
    
    def test_data_directory_exists(self):
        """Test that data directory exists."""
        data_dir = Path(__file__).parent.parent / "data"
        assert data_dir.exists()
        assert data_dir.is_dir()

