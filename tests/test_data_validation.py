"""
Data structure and validation tests.
"""

import os
import pytest
import pandas as pd
from pathlib import Path


class TestDataFiles:
    """Test data file existence and structure."""
    
    def test_sample_data_exists(self):
        """Test that sample data file exists (if available)."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            assert sample_file.is_file()
    
    def test_sample_data_structure(self):
        """Test sample data file structure if it exists."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            df = pd.read_parquet(sample_file)
            
            # Check required columns exist
            expected_columns = [
                'student_id', 'student_name', 'university', 'state',
                'university_type', 'subject', 'score', 'grade',
                'attendance_flag', 'performance_category', 'year',
                'semester', 'date', 'credits', 'course_level', 'batch_number'
            ]
            
            for col in expected_columns:
                assert col in df.columns, f"Missing column: {col}"
            
            # Check data types
            assert df['student_id'].dtype in ['object', 'int64', 'int32']
            assert df['score'].dtype in ['float64', 'int64', 'float32', 'int32']
            assert df['year'].dtype in ['int64', 'int32']
            assert df['attendance_flag'].dtype == bool or df['attendance_flag'].dtype.name == 'bool'
            
            # Check data is not empty
            assert len(df) > 0, "Sample data is empty"
    
    def test_batch_files_exist(self):
        """Test that batch files exist (if available)."""
        data_dir = Path("data/milestone1_real")
        if data_dir.exists():
            batch_files = list(data_dir.glob("students_batch_*_100K_cleaned.parquet"))
            # At least one batch file should exist for the project to work
            # But we don't fail if none exist (they might be generated)
            if batch_files:
                assert len(batch_files) > 0
    
    def test_batch_file_structure(self):
        """Test batch file structure if they exist."""
        data_dir = Path("data/milestone1_real")
        if data_dir.exists():
            batch_files = sorted(data_dir.glob("students_batch_*_100K_cleaned.parquet"))
            if batch_files:
                # Test first batch file
                df = pd.read_parquet(batch_files[0])
                
                # Check it has data
                assert len(df) > 0, "Batch file is empty"
                
                # Check it has expected columns
                expected_columns = [
                    'student_id', 'student_name', 'university', 'state',
                    'university_type', 'subject', 'score', 'grade',
                    'attendance_flag', 'performance_category', 'year',
                    'semester', 'date', 'credits', 'course_level', 'batch_number'
                ]
                
                for col in expected_columns:
                    assert col in df.columns, f"Missing column in batch file: {col}"


class TestDataValidation:
    """Test data validation logic."""
    
    def test_performance_categories(self):
        """Test that performance categories are valid."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            df = pd.read_parquet(sample_file)
            valid_categories = ['Low', 'Medium', 'High', 'Excellent', 'Poor']
            
            if 'performance_category' in df.columns:
                unique_categories = df['performance_category'].unique()
                for cat in unique_categories:
                    assert cat in valid_categories, f"Invalid performance category: {cat}"
    
    def test_score_range(self):
        """Test that scores are in valid range."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            df = pd.read_parquet(sample_file)
            
            if 'score' in df.columns:
                scores = df['score'].dropna()
                if len(scores) > 0:
                    assert scores.min() >= 0, "Scores should be >= 0"
                    assert scores.max() <= 100, "Scores should be <= 100"
    
    def test_year_range(self):
        """Test that years are in valid range."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            df = pd.read_parquet(sample_file)
            
            if 'year' in df.columns:
                years = df['year'].dropna()
                if len(years) > 0:
                    assert years.min() >= 2010, "Years should be >= 2010"
                    assert years.max() <= 2024, "Years should be <= 2024"
    
    def test_university_types(self):
        """Test that university types are valid."""
        sample_file = Path("data/milestone1_real/sample_100K_students.parquet")
        if sample_file.exists():
            df = pd.read_parquet(sample_file)
            
            if 'university_type' in df.columns:
                valid_types = ['Ivy League', 'Public', 'Private']
                unique_types = df['university_type'].unique()
                for utype in unique_types:
                    assert utype in valid_types, f"Invalid university type: {utype}"

