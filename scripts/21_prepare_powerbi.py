import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

# ============================================================
# LOAD THE DATASET WITH SKILLS
# ============================================================

df = pd.read_csv(
    DATA_DIR / "04_analyst_jobs_skills.csv"
)

print("=" * 70)
print("PREPARING FINAL POWER BI DATASET")
print("=" * 70)


# ============================================================
# ADD LOCATION INFORMATION
# ============================================================

location_df = pd.read_csv(
    DATA_DIR / "08_analyst_jobs_location_clean.csv"
)

# We only need the location fields from this file
location_fields = location_df[
    [
        "job_id",
        "location_raw",
        "city",
        "state"
    ]
].copy()


# Make sure job_id has the same data type
df["job_id"] = df["job_id"].astype(str)

location_fields["job_id"] = (
    location_fields["job_id"]
    .astype(str)
)


# ============================================================
# MERGE LOCATION DATA
# ============================================================

df = df.merge(
    location_fields,
    on="job_id",
    how="left"
)


# ============================================================
# SELECT FINAL COLUMNS
# ============================================================

final_columns = [
    "job_id",
    "title",
    "job_category",
    "company",
    "location_raw",
    "city",
    "state",
    "salary_min",
    "salary_max",
    "salary_mid",
    "has_salary",
    "created",
    "posted_year",
    "search_term",
    "SQL",
    "Python",
    "Excel",
    "Power BI",
    "Tableau",
    "AWS",
    "Azure",
    "GCP",
    "Snowflake",
    "Databricks",
    "ETL",
    "Statistics",
    "Machine Learning"
]


df = df[
    final_columns
].copy()


# ============================================================
# FINAL QUALITY CHECK
# ============================================================

print("\nFinal shape:")
print(df.shape)


print("\nFinal columns:")

print(
    df.columns.tolist()
)


print("\nDuplicate job IDs:")

print(
    df["job_id"].duplicated().sum()
)


print("\nMissing values:")

print(
    df.isnull().sum()
)


# ============================================================
# SAVE FINAL DATASET
# ============================================================

OUTPUT_FILE = DATA_DIR / "16_analyst_jobs_final.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("FINAL POWER BI DATASET CREATED")
print("=" * 70)

print("\nFile:")
print(OUTPUT_FILE)