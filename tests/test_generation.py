"""
Test script for modified data generation
Generates 1K students to verify the changes work correctly
"""

from scripts.real_data_milestone1 import RealDataMilestone1

# Create generator with small batch for testing
generator = RealDataMilestone1(
    target_students=1000,
    batch_size=1000,
    start_year=2010,
    end_year=2024
)

print("🧪 Starting test generation with 1K students...")
print("=" * 60)

# Get university profiles (skip IPEDS download for test)
university_profiles = generator.create_university_profiles()

# Generate one test batch
batch_records = generator.generate_student_batch(1, university_profiles, 1)
print(f"✅ Generated {len(batch_records)} records")

# Process batch (will write Parquet)
df_test = generator.process_batch_data(batch_records, 1)

print("\n📊 Test Results:")
print(f"Total records: {len(df_test):,}")
print(f"Unique students: {df_test['student_id'].nunique():,}")
print(f"Unique majors: {df_test['major'].nunique()}")
print(f"\nMajor distribution:")
print(df_test['major'].value_counts())

# Critical check: Verify each student has only ONE year
print("\n🔍 Critical Check: Years per student")
years_per_student = df_test.groupby('student_id')['year'].nunique()
print(f"Students with 1 year: {(years_per_student == 1).sum()}")
print(f"Students with > 1 year: {(years_per_student > 1).sum()}")

if (years_per_student > 1).sum() > 0:
    print("❌ ERROR: Some students span multiple years!")
    print(years_per_student[years_per_student > 1].head())
else:
    print("✅ SUCCESS: All students in single year!")

# Check subjects per student
subjects_per_student = df_test.groupby('student_id')['subject'].nunique()
print(f"\nSubjects per student (8-12 expected):")
print(subjects_per_student.value_counts().sort_index())

print("\n✅ Test complete! Check: data/milestone1_real/students_batch_01_100K_cleaned.parquet")
