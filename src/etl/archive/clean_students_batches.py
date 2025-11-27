import os
import sys
import re
import json
from typing import Dict, List

import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "milestone1_real")


UNIVERSITY_TO_STATE: Dict[str, str] = {
    # Ivy League
    "Brown University": "Rhode Island",
    "Columbia University": "New York",
    "Cornell University": "New York",
    "Dartmouth College": "New Hampshire",
    "Harvard University": "Massachusetts",
    "Princeton University": "New Jersey",
    "University of Pennsylvania": "Pennsylvania",
    "Yale University": "Connecticut",
    # Private / Public well-known
    "Stanford University": "California",
    "Massachusetts Institute of Technology": "Massachusetts",
    "California Institute of Technology": "California",
    "Carnegie Mellon University": "Pennsylvania",
    "Duke University": "North Carolina",
    "Emory University": "Georgia",
    "Georgetown University": "District of Columbia",
    "Georgia Institute of Technology": "Georgia",
    "Indiana University Bloomington": "Indiana",
    "Johns Hopkins University": "Maryland",
    "Michigan State University": "Michigan",
    "New York University": "New York",
    "Northwestern University": "Illinois",
    "Ohio State University": "Ohio",
    "Pennsylvania State University": "Pennsylvania",
    "Purdue University": "Indiana",
    "Rice University": "Texas",
    "Rutgers University": "New Jersey",
    "Texas A&M University": "Texas",
    "University of California, Berkeley": "California",
    "University of California, Davis": "California",
    "University of California, Irvine": "California",
    "University of California, Los Angeles": "California",
    "University of California, San Diego": "California",
    "University of California, Santa Barbara": "California",
    "University of Chicago": "Illinois",
    "University of Florida": "Florida",
    "University of Illinois Urbana-Champaign": "Illinois",
    "University of Maryland": "Maryland",
    "University of Michigan": "Michigan",
    "University of Minnesota": "Minnesota",
    "University of North Carolina": "North Carolina",
    "University of Notre Dame": "Indiana",
    "University of Rochester": "New York",
    "University of Southern California": "California",
    "University of Texas at Austin": "Texas",
    "University of Virginia": "Virginia",
    "University of Washington": "Washington",
    "University of Wisconsin-Madison": "Wisconsin",
    "Vanderbilt University": "Tennessee",
    "Washington University in St. Louis": "Missouri",
    "Boston University": "Massachusetts",
}


UNIVERSITY_TO_TYPE: Dict[str, str] = {
    # Ivy League
    "Brown University": "Ivy League",
    "Columbia University": "Ivy League",
    "Cornell University": "Ivy League",
    "Dartmouth College": "Ivy League",
    "Harvard University": "Ivy League",
    "Princeton University": "Ivy League",
    "University of Pennsylvania": "Ivy League",
    "Yale University": "Ivy League",
    # Publics
    "Georgia Institute of Technology": "Public",
    "Indiana University Bloomington": "Public",
    "Michigan State University": "Public",
    "Ohio State University": "Public",
    "Pennsylvania State University": "Public",
    "Purdue University": "Public",
    "Rutgers University": "Public",
    "Texas A&M University": "Public",
    "University of California, Berkeley": "Public",
    "University of California, Davis": "Public",
    "University of California, Irvine": "Public",
    "University of California, Los Angeles": "Public",
    "University of California, San Diego": "Public",
    "University of California, Santa Barbara": "Public",
    "University of Florida": "Public",
    "University of Illinois Urbana-Champaign": "Public",
    "University of Maryland": "Public",
    "University of Michigan": "Public",
    "University of Minnesota": "Public",
    "University of North Carolina": "Public",
    "University of Texas at Austin": "Public",
    "University of Virginia": "Public",
    "University of Washington": "Public",
    "University of Wisconsin-Madison": "Public",
    # Privates (non-Ivy)
    "Stanford University": "Private",
    "Massachusetts Institute of Technology": "Private",
    "California Institute of Technology": "Private",
    "Carnegie Mellon University": "Private",
    "Duke University": "Private",
    "Emory University": "Private",
    "Georgetown University": "Private",
    "Johns Hopkins University": "Private",
    "New York University": "Private",
    "Northwestern University": "Private",
    "Rice University": "Private",
    "University of Chicago": "Private",
    "University of Notre Dame": "Private",
    "University of Rochester": "Private",
    "University of Southern California": "Private",
    "Vanderbilt University": "Private",
    "Washington University in St. Louis": "Private",
    "Boston University": "Private",
}


def generate_student_aliases(series: pd.Series) -> pd.Series:
    unique_names = pd.Index(series.fillna("").unique())
    # Map any name that matches Unk_Student_\d+ to Student_00001-style sequential ids based on first appearance
    unk_mask = unique_names.str.match(r"^Unk_Student_\d+$")
    unk_names = unique_names[unk_mask]
    mapping: Dict[str, str] = {}
    for idx, _name in enumerate(unk_names, start=1):
        mapping[_name] = f"Student_{idx:05d}"
    # Non-unk names remain as-is
    return series.map(lambda x: mapping.get(x, x))


def coerce_boolean(series: pd.Series) -> pd.Series:
    truthy = {True, "true", "True", "1", 1, "Yes", "YES", "yes"}
    falsy = {False, "false", "False", "0", 0, "No", "NO", "no"}
    def to_bool(v):
        if pd.isna(v):
            return False
        if v in truthy:
            return True
        if v in falsy:
            return False
        if isinstance(v, str):
            vs = v.strip().lower()
            if vs in {"t", "y"}:
                return True
            if vs in {"f", "n"}:
                return False
        return bool(v)
    return series.apply(to_bool)


def standardize_performance(series: pd.Series) -> pd.Series:
    mapping = {
        "poor": "Poor",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "excellent": "Excellent",
    }
    return series.astype(str).str.strip().str.lower().map(mapping).fillna(series)


def ensure_iso_dates(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
    return parsed.dt.strftime("%Y-%m-%d")


def clean_batch(input_path: str, output_path: str) -> None:
    df = pd.read_csv(
        input_path,
        dtype={
            "student_id": str,
            "name": str,
            "university": str,
            "university_state": str,
            "university_type": str,
            "subject": str,
            "score": float,
            "grade": str,
            "attendance": object,
            "performance_category": str,
            "year": int,
            "semester": str,
            "date": str,
            "credits": float,
            "course_level": str,
            "ipeds_institutional_factor": float,
            "batch_number": int,
        },
        low_memory=False,
    )

    # Rename columns to snake_case where requested
    rename_map = {
        "name": "student_name",
        "university_state": "state",
        "attendance": "attendance_flag",
        # keep ipeds_institutional_factor and batch_number as-is
    }
    df = df.rename(columns=rename_map)

    # Student names anonymization for Unk_Student_* only
    df["student_name"] = generate_student_aliases(df["student_name"]) if "student_name" in df else df["student_name"]

    # University state mapping; leave Unknown if not mapped
    df["state"] = df.apply(
        lambda r: UNIVERSITY_TO_STATE.get(str(r["university"]).strip(), r.get("state", "Unknown")), axis=1
    )

    # University type mapping; prefer mapping over existing value
    df["university_type"] = df["university"].map(UNIVERSITY_TO_TYPE).fillna(df.get("university_type"))

    # Attendance to boolean
    df["attendance_flag"] = coerce_boolean(df["attendance_flag"]).astype(bool)

    # Performance categories: keep only Low, Medium, High, Excellent, Poor
    df["performance_category"] = standardize_performance(df["performance_category"])

    # Dates to ISO
    df["date"] = ensure_iso_dates(df["date"])

    # Final column order
    final_cols = [
        "student_id",
        "student_name",
        "university",
        "state",
        "university_type",
        "subject",
        "score",
        "grade",
        "attendance_flag",
        "performance_category",
        "year",
        "semester",
        "date",
        "credits",
        "course_level",
        "batch_number",
    ]
    # Ensure columns exist (some datasets may miss a column); keep extra columns at end
    existing_final = [c for c in final_cols if c in df.columns]
    extra_cols = [c for c in df.columns if c not in existing_final]
    ordered_cols = existing_final + extra_cols
    df = df[ordered_cols]

    # Write cleaned batch
    df.to_csv(output_path, index=False)


def main():
    input_batches: List[str] = [
        os.path.join(DATA_DIR, f"students_batch_{i:02d}_100K.csv") for i in range(1, 11)
    ]
    output_batches: List[str] = [
        os.path.join(DATA_DIR, f"students_batch_{i:02d}_100K_cleaned.csv") for i in range(1, 11)
    ]

    for in_path, out_path in zip(input_batches, output_batches):
        if not os.path.exists(in_path):
            print(f"Warning: missing input batch {in_path}")
            continue
        print(f"Cleaning {os.path.basename(in_path)} -> {os.path.basename(out_path)}")
        clean_batch(in_path, out_path)

    # Concatenate cleaned batches
    existing_outputs = [p for p in output_batches if os.path.exists(p)]
    if not existing_outputs:
        print("No cleaned batches produced. Exiting.")
        sys.exit(1)

    frames = [pd.read_csv(p, low_memory=False) for p in existing_outputs]
    combined = pd.concat(frames, ignore_index=True)
    combined_out = os.path.join(DATA_DIR, "cleaned_students.csv")
    combined.to_csv(combined_out, index=False)
    print(f"Wrote combined cleaned file: {combined_out}")

    # Delete old combined raw file if present
    raw_combined = os.path.join(DATA_DIR, "student_performance_1M_real_data.csv")
    if os.path.exists(raw_combined):
        try:
            os.remove(raw_combined)
            print(f"Deleted old combined file: {raw_combined}")
        except Exception as e:
            print(f"Could not delete {raw_combined}: {e}")


if __name__ == "__main__":
    main()


