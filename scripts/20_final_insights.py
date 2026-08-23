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

jobs = pd.read_csv(
    DATA_DIR / "04_analyst_jobs_skills.csv"
)

locations = pd.read_csv(
    DATA_DIR / "08_analyst_jobs_location_clean.csv"
)

salary = pd.read_csv(
    DATA_DIR / "05_analyst_salary_clean.csv"
)

print("=" * 70)
print("FINAL ANALYST JOB MARKET INSIGHTS")
print("=" * 70)


# ============================================================
# 1. TOTAL JOBS
# ============================================================

print("\n1. TOTAL JOB POSTINGS")

print(
    "Total unique jobs:",
    len(jobs)
)


# ============================================================
# 2. TOP ANALYST CATEGORY
# ============================================================

analyst_categories = jobs[
    ~jobs["job_category"].isin([
        "Non-Analyst Role",
        "Adjacent Data / Tech Role"
    ])
]

category_counts = (
    analyst_categories[
        "job_category"
    ]
    .value_counts()
)


print("\n2. TOP ANALYST CATEGORIES")

print(
    category_counts.head(10)
)


# ============================================================
# 3. TOP CITIES
# ============================================================

city_counts = (
    locations[
        locations["city"] != "Nationwide"
    ]["city"]
    .value_counts()
)


print("\n3. TOP CITIES")

print(
    city_counts.head(10)
)


# ============================================================
# 4. TOP SKILLS
# ============================================================

skills = [
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


skill_counts = {
    skill: jobs[skill].sum()
    for skill in skills
}


skill_counts = (
    pd.Series(skill_counts)
    .sort_values(
        ascending=False
    )
)


print("\n4. TOP SKILLS")

print(
    skill_counts.head(10)
)


# ============================================================
# 5. SALARY
# ============================================================

print("\n5. SALARY")

print(
    "Salary records:",
    len(salary)
)

print(
    "Median salary:",
    salary["salary_mid"].median()
)

print(
    "Average salary:",
    salary["salary_mid"].mean()
)


# ============================================================
# 6. SALARY BY CATEGORY
# ============================================================

salary_category = (
    salary[
        ~salary["job_category"].isin([
            "Non-Analyst Role",
            "Adjacent Data / Tech Role"
        ])
    ]
    .groupby("job_category")
    .agg(
        jobs=("salary_mid", "count"),
        median_salary=("salary_mid", "median")
    )
    .reset_index()
)

salary_category = salary_category[
    salary_category["jobs"] >= 10
].sort_values(
    "median_salary",
    ascending=False
)


print("\n6. SALARY BY ANALYST CATEGORY")

print(
    salary_category
)


# ============================================================
# 7. DATA ANALYST SKILLS
# ============================================================

data_analyst = jobs[
    jobs["job_category"] == "Data Analyst"
]

da_skill_counts = {
    skill: data_analyst[skill].sum()
    for skill in skills
}

da_skill_counts = (
    pd.Series(da_skill_counts)
    .sort_values(
        ascending=False
    )
)


print("\n7. DATA ANALYST SKILLS")

print(
    da_skill_counts.head(10)
)


print("\n" + "=" * 70)
print("INSIGHT EXTRACTION COMPLETE")
print("=" * 70)