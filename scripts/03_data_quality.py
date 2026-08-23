import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"


# ============================================================
# LOAD DATA
# ============================================================

INPUT_FILE = DATA_DIR / "01_analyst_jobs_master_raw.csv"

df = pd.read_csv(INPUT_FILE)


print("=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)


# ============================================================
# DATASET OVERVIEW
# ============================================================

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ============================================================
# MISSING VALUES
# ============================================================

print("\nMissing values:")
print(df.isnull().sum())

print("\nMissing percentage:")
print(
    (df.isnull().mean() * 100).round(2)
)


# ============================================================
# DUPLICATES
# ============================================================

print("\nDuplicate job IDs:")
print(
    df["job_id"].duplicated().sum()
)


# ============================================================
# UNIQUE VALUES
# ============================================================

print("\nUnique companies:")
print(
    df["company"].nunique()
)

print("\nUnique locations:")
print(
    df["location"].nunique()
)


# ============================================================
# DATE RANGE
# ============================================================

print("\nDate range:")

print(
    "Earliest:",
    df["created"].min()
)

print(
    "Latest:",
    df["created"].max()
)


print("\n" + "=" * 60)
print("DATA QUALITY CHECK COMPLETE")
print("=" * 60)