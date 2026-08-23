import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"


# ============================================================
# LOAD RAW DATA
# ============================================================

INPUT_FILE = DATA_DIR / "01_analyst_jobs_master_raw.csv"

df = pd.read_csv(INPUT_FILE)


print("=" * 60)
print("MASTER RAW DATASET")
print("=" * 60)


# ============================================================
# BASIC STANDARDIZATION
# ============================================================

# Make sure job_id is treated consistently
df["job_id"] = df["job_id"].astype(str)


# Fill missing search term
df["search_term"] = df["search_term"].fillna("Analyst")


# Create salary availability flag
df["has_salary"] = (
    df["salary_min"].notna() |
    df["salary_max"].notna()
)


# Convert date
df["created"] = pd.to_datetime(
    df["created"],
    errors="coerce",
    utc=True
)


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print(
    "\nDuplicate job IDs:",
    df["job_id"].duplicated().sum()
)

print("\nSearch terms:")
print(df["search_term"].value_counts())

print("\nSalary availability:")
print(df["has_salary"].value_counts())

print("\nSalary availability %:")
print(
    round(
        df["has_salary"].mean() * 100,
        2
    ),
    "%"
)


# ============================================================
# SAVE MASTER RAW DATASET
# ============================================================

OUTPUT_FILE = DATA_DIR / "01_analyst_jobs_master_raw.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved:")
print(OUTPUT_FILE)