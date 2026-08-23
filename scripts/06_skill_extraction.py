import pandas as pd
import re
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

# ============================================================
# 1. LOAD CLEAN DATA
# ============================================================

INPUT_FILE = DATA_DIR / "03_analyst_jobs_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SKILL EXTRACTION")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 2. MAKE DESCRIPTION SEARCHABLE
# ============================================================

df["description_clean"] = (
    df["description"]
    .fillna("")
    .astype(str)
    .str.lower()
)


# ============================================================
# 3. DEFINE SKILLS
# ============================================================

skills = {
    "SQL": r"\bsql\b",

    "Python": r"\bpython\b",

    "Excel": r"\bexcel\b|microsoft excel",

    "Power BI": r"\bpower\s*bi\b",

    "Tableau": r"\btableau\b",

    "R": (
    r"\br programming\b|"
    r"\br language\b|"
    r"\br statistical\b|"
    r"\brstudio\b|"
    r"\busing r\b|"
    r"\bskills in r\b"
),

    "SAS": r"\bsas\b",

    "AWS": r"\baws\b|amazon web services",

    "Azure": r"\bazure\b",

    "GCP": r"\bgcp\b|google cloud platform",

    "Snowflake": r"\bsnowflake\b",

    "Databricks": r"\bdatabricks\b",

    "ETL": r"\betl\b|extract transform load",

    "Statistics": r"\bstatistics\b|\bstatistical\b",

    "Machine Learning": (
        r"\bmachine learning\b|"
        r"\bml\b"
    )
}


# ============================================================
# 4. CREATE SKILL COLUMNS
# ============================================================

for skill, pattern in skills.items():

    df[skill] = (
        df["description_clean"]
        .str.contains(
            pattern,
            regex=True,
            case=False,
            na=False
        )
        .astype(int)
    )


# ============================================================
# 5. CHECK RESULTS
# ============================================================

print("\nSkill counts:")

for skill in skills:

    count = df[skill].sum()

    percentage = (
        count / len(df) * 100
    )

    print(
        f"{skill:20} "
        f"{count:5} jobs "
        f"({percentage:6.2f}%)"
    )


# ============================================================
# 6. SAVE
# ============================================================

OUTPUT_FILE = DATA_DIR / "04_analyst_jobs_skills.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSaved:")
print(OUTPUT_FILE)