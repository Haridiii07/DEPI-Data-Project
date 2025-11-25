import os
import json
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "milestone1_real")
INPUT = os.path.join(DATA_DIR, "cleaned_students.csv")
OUTPUT = os.path.join(DATA_DIR, "summary_1M_real_data.csv")


def main() -> None:
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Missing input file: {INPUT}")

    # Accumulators
    total_records = 0
    unique_students = set()
    unique_universities = set()
    unique_subjects = set()
    attendance_true = 0
    performance_counts = {}
    university_counts = {}
    year_min = None
    year_max = None

    for chunk in pd.read_csv(INPUT, chunksize=250_000, low_memory=False):
        total_records += len(chunk)

        if "student_id" in chunk.columns:
            unique_students.update(chunk["student_id"].astype(str).unique())
        if "university" in chunk.columns:
            vals = chunk["university"].astype(str)
            unique_universities.update(vals.unique())
            for u, c in vals.value_counts().items():
                university_counts[u] = university_counts.get(u, 0) + int(c)
        if "subject" in chunk.columns:
            unique_subjects.update(chunk["subject"].astype(str).unique())
        if "attendance_flag" in chunk.columns:
            attendance_true += chunk["attendance_flag"].astype(bool).sum()
        if "performance_category" in chunk.columns:
            for k, c in chunk["performance_category"].value_counts().items():
                performance_counts[k] = performance_counts.get(k, 0) + int(c)
        if "year" in chunk.columns:
            yr_min = chunk["year"].min()
            yr_max = chunk["year"].max()
            year_min = yr_min if year_min is None else min(year_min, yr_min)
            year_max = yr_max if year_max is None else max(year_max, yr_max)

    attendance_rate = attendance_true / total_records if total_records else 0.0

    # Prepare summary rows
    rows = [
        [
            "total_records",
            "unique_students",
            "unique_universities",
            "unique_subjects",
            "year_range",
            "attendance_rate",
            "performance_distribution",
            "university_distribution",
        ],
        [
            total_records,
            len(unique_students),
            len(unique_universities),
            len(unique_subjects),
            f"{year_min}-{year_max}",
            round(attendance_rate, 4),
            json.dumps(performance_counts, ensure_ascii=False),
            json.dumps(university_counts, ensure_ascii=False),
        ],
    ]

    import csv

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Wrote summary: {OUTPUT}")


if __name__ == "__main__":
    main()


