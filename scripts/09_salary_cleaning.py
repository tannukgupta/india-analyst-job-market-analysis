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

INPUT_FILE = DATA_DIR / "04_analyst_jobs_skills.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SALARY DATA QUALITY CHECK")
print("=" * 70)


# ============================================================
# SALARY DATASET
# ============================================================

salary_df = df[df["has_salary"] == True].copy()

print("\nJobs with salary:", len(salary_df))


# ============================================================
# CREATE SALARY MIDPOINT
# ============================================================

salary_df["salary_mid"] = (
    salary_df["salary_min"] +
    salary_df["salary_max"]
) / 2


# ============================================================
# FLAG SUSPICIOUSLY LOW VALUES
# ============================================================

salary_df["salary_suspicious_low"] = (
    salary_df["salary_mid"] < 100000
)


print("\nSuspicious low salary records:")

print(
    salary_df["salary_suspicious_low"]
    .value_counts()
)


# ============================================================
# SHOW SUSPICIOUS RECORDS
# ============================================================

print("\nSuspicious records:")

print(
    salary_df[
        salary_df["salary_suspicious_low"]
    ][
        [
            "title",
            "job_category",
            "salary_min",
            "salary_max",
            "salary_mid"
        ]
    ]
    .sort_values("salary_mid")
    .head(30)
    .to_string(index=False)
)


# ============================================================
# CREATE CLEAN SALARY DATASET
# ============================================================

salary_clean = salary_df[
    ~salary_df["salary_suspicious_low"]
].copy()


print("\nOriginal salary records:")
print(len(salary_df))

print("\nRecords after excluding suspicious values:")
print(len(salary_clean))


# ============================================================
# CLEAN SALARY STATISTICS
# ============================================================

print("\nClean salary statistics:")

print(
    salary_clean["salary_mid"].describe()
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE = DATA_DIR / "05_analyst_salary_clean.csv"

salary_clean.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved:")
print(OUTPUT_FILE)