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

skills = [
    "SQL",
    "Python",
    "Excel",
    "Power BI",
    "Tableau",
    "R",
    "SAS",
    "AWS",
    "Azure",
    "GCP",
    "Snowflake",
    "Databricks",
    "ETL",
    "Statistics",
    "Machine Learning"
]


print("=" * 70)
print("SKILL VALIDATION")
print("=" * 70)


for skill in skills:

    print("\n" + "-" * 70)
    print("SKILL:", skill)

    matches = df[df[skill] == 1]

    print("Number of matches:", len(matches))

    print("\nSample job titles:")

    print(
        matches["title"]
        .head(10)
        .to_string(index=False)
    )


# ------------------------------------------------------------
# SPECIAL CHECK FOR R
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CHECKING R")
print("=" * 70)

r_jobs = df[df["R"] == 1]

print("Jobs matched as R:", len(r_jobs))

print("\nSample descriptions containing R:")

for description in r_jobs["description"].head(10):

    safe_text = str(description[:500]).encode(
        "ascii",
        errors="replace"
    ).decode("ascii")

    print("\n", safe_text)