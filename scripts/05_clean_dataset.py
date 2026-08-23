import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

# ============================================================
# 1. LOAD DATA
# ============================================================

INPUT_FILE = DATA_DIR / "02_analyst_jobs_classified.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("ANALYST JOB MARKET - DATA CLEANING")
print("=" * 70)

print("\nOriginal dataset shape:")
print(df.shape)


# ============================================================
# 2. CHECK COLUMNS
# ============================================================

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(df.isnull().sum())


# ============================================================
# 4. CREATE SALARY AVAILABILITY FLAG
# ============================================================

df["has_salary"] = (
    df["salary_min"].notna()
    |
    df["salary_max"].notna()
)

print("\nSalary availability:")
print(df["has_salary"].value_counts())


# ============================================================
# 5. CREATE SALARY MIDPOINT
# ============================================================

df["salary_mid"] = (
    df["salary_min"] +
    df["salary_max"]
) / 2


# ============================================================
# 6. CONVERT CREATED TO DATETIME
# ============================================================

df["created"] = pd.to_datetime(
    df["created"],
    errors="coerce",
    utc=True
)

print("\nCreated column type:")
print(df["created"].dtype)


# ============================================================
# 7. CREATE DATE VARIABLES
# ============================================================

df["posted_year"] = df["created"].dt.year

df["posted_month"] = df["created"].dt.month

df["posted_month_name"] = (
    df["created"].dt.month_name()
)

df["posted_month_period"] = (
    df["created"].dt.to_period("M")
)


# ============================================================
# 8. CHECK SALARY CALCULATIONS
# ============================================================

print("\nSalary sample:")

print(
    df[
        [
            "salary_min",
            "salary_max",
            "salary_mid",
            "has_salary"
        ]
    ].head(20)
)


# ============================================================
# 9. CHECK DATE RANGE
# ============================================================

print("\nDate range:")

print("Earliest:")
print(df["created"].min())

print("Latest:")
print(df["created"].max())


# ============================================================
# 10. CHECK JOB CATEGORIES
# ============================================================

print("\nJob categories:")

print(
    df["job_category"]
    .value_counts()
)


# ============================================================
# 11. SAVE CLEAN DATA
# ============================================================

OUTPUT_FILE = DATA_DIR / "03_analyst_jobs_clean.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("CLEANING STEP COMPLETED")
print("=" * 70)

print("\nFinal shape:")
print(df.shape)

print("\nSaved file:")
print(OUTPUT_FILE)