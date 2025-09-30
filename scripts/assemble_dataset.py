"""
Assemble cleaned batch ZIP files into a single CSV for analysis.

This script discovers batch archives like:
  data/milestone1_real/students_batch_01_100K_cleaned.zip ... 10

It extracts the underlying CSVs (without writing intermediates), concatenates
them in numeric order, and writes:
  data/milestone1_real/cleaned_students.csv

Optionally, it can also create a sample CSV by uniformly sampling a fixed
number of rows from each batch.

Usage (from project root):
  python scripts/assemble_dataset.py --create-sample --rows-per-batch 10000

Dependencies: pandas
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import zipfile
from glob import glob
from typing import List

import pandas as pd


DATA_DIR = os.path.join("data", "milestone1_real")
OUTPUT_FULL = os.path.join(DATA_DIR, "cleaned_students.csv")
OUTPUT_SAMPLE = os.path.join(DATA_DIR, "sample_100K_students.csv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble cleaned batch ZIPs into a single CSV")
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="Additionally create a sample CSV by sampling per-batch rows.",
    )
    parser.add_argument(
        "--rows-per-batch",
        type=int,
        default=10000,
        help="Number of rows to sample from each batch for the sample CSV (default: 10000)",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=7,
        help="Random seed for reproducible sampling (default: 7)",
    )
    return parser.parse_args()


def batch_sort_key(path: str) -> int:
    """Extract two-digit batch number from the archive name for ordering."""
    match = re.search(r"students_batch_(\d{2})_100K_cleaned\.zip$", os.path.basename(path))
    return int(match.group(1)) if match else 9999


def find_batch_archives() -> List[str]:
    pattern = os.path.join(DATA_DIR, "students_batch_*_100K_cleaned.zip")
    candidates = glob(pattern)
    zips = [z for z in candidates if re.search(r"students_batch_\d{2}_100K_cleaned\.zip$", os.path.basename(z))]
    return sorted(zips, key=batch_sort_key)


def read_csv_from_zip(zip_path: str) -> pd.DataFrame:
    """Read the single CSV contained in a ZIP file into a DataFrame without extracting to disk."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise FileNotFoundError(f"No CSV found inside: {zip_path}")
        if len(csv_names) > 1:
            # Pick the first CSV deterministically if multiple are present
            csv_names.sort()
        with zf.open(csv_names[0]) as fp:
            return pd.read_csv(io.TextIOWrapper(fp, encoding="utf-8"))


def assemble(create_sample: bool, rows_per_batch: int, random_seed: int) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    archives = find_batch_archives()
    if not archives:
        raise FileNotFoundError(
            f"No batch ZIPs found in {DATA_DIR}. Expected files like 'students_batch_01_100K_cleaned.zip'."
        )

    full_frames: List[pd.DataFrame] = []
    sample_frames: List[pd.DataFrame] = []

    for archive in archives:
        df = read_csv_from_zip(archive)
        full_frames.append(df)

        if create_sample:
            n = min(rows_per_batch, len(df))
            sample_frames.append(df.sample(n=n, random_state=random_seed))

    full_df = pd.concat(full_frames, ignore_index=True)
    full_df.to_csv(OUTPUT_FULL, index=False)
    print(f"Saved full dataset: {OUTPUT_FULL} (rows: {len(full_df):,})")

    if create_sample:
        sample_df = pd.concat(sample_frames, ignore_index=True)
        sample_df.to_csv(OUTPUT_SAMPLE, index=False)
        print(f"Saved sample dataset: {OUTPUT_SAMPLE} (rows: {len(sample_df):,})")


def main() -> None:
    args = parse_args()
    try:
        assemble(args.create_sample, args.rows_per_batch, args.random_seed)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


