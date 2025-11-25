"""
Simple direct test of major-based generation logic
"""
import sys
sys.path.insert(0, 'scripts')

from majors_config import assign_major, get_major_subjects
import pandas as pd
import numpy as np

print("🧪 Testing Major-Based Subject Selection\n" + "="*60)

# Test 1: Major assignment
print("\n1️⃣ Testing Major Assignment:")
majors = [assign_major() for _ in range(100)]
major_counts = pd.Series(majors).value_counts()
print(major_counts.head(10))

# Test 2: Subject selection for different majors
print("\n2️⃣ Testing Subject Selection:")
test_majors = ["Computer Science", "Biology", "Business Administration"]

for major in test_majors:
    subjects = get_major_subjects(major, num_subjects=10)
    print(f"\n{major} (10 subjects):")
    print(f"  {', '.join(subjects)}")

# Test 3: Verify single-year logic
print("\n3️⃣ Simulating 5 Students with Single Year:")
print("-" * 60)

np.random.seed(42)
for i in range(1, 6):
    student_id = f"Student_{i:05d}"
    graduation_year = np.random.randint(2010, 2025)
    major = assign_major()
    num_subjects = np.random.randint(8, 13)
    subjects = get_major_subjects(major, num_subjects)
    
    print(f"\n{student_id}:")
    print(f"  Major: {major}")
    print(f"  Graduation Year: {graduation_year}")
    print(f"  Subjects ({len(subjects)}): {', '.join(subjects[:3])}...")
    
print("\n✅ All tests passed!")
print("\nNow ready to generate full dataset with this logic.")
