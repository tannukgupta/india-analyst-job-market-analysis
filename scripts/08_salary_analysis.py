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

INPUT_FILE = DATA_DIR / "04_analyst_jobs_skills.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SALARY ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 2. SALARY AVAILABILITY
# ============================================================

print("\nSalary availability:")

print(
    df["has_salary"]
    .value_counts()
)


salary_jobs = df[df["has_salary"] == True].copy()

print("\nJobs with salary information:")
print(len(salary_jobs))


# ============================================================
# 3. SALARY BASIC STATISTICS
# ============================================================

print("\nSalary statistics:")

print(
    salary_jobs["salary_mid"]
    .describe()
)

print("\nSalary range distribution:")

print(
    salary_jobs["salary_mid"]
    .quantile(
        [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )
)


# ============================================================
# 4. CHECK EXTREME VALUES
# ============================================================

lowest = (
    salary_jobs[
        [
            "title",
            "salary_min",
            "salary_max",
            "salary_mid"
        ]
    ]
    .sort_values("salary_mid")
    .head(10)
)

print("\nLowest salaries:")
print(
    lowest.to_string(index=False)
    .encode("ascii", errors="replace")
    .decode("ascii")
)


highest = (
    salary_jobs[
        [
            "title",
            "salary_min",
            "salary_max",
            "salary_mid"
        ]
    ]
    .sort_values(
        "salary_mid",
        ascending=False
    )
    .head(10)
)

print("\nHighest salaries:")
print(
    highest.to_string(index=False)
    .encode("ascii", errors="replace")
    .decode("ascii")
)


# ============================================================
# 5. SALARY BY JOB CATEGORY
# ============================================================

category_salary = (
    salary_jobs
    .groupby("job_category")
    .agg(
        jobs_with_salary=("salary_mid", "count"),
        average_salary=("salary_mid", "mean"),
        median_salary=("salary_mid", "median"),
        minimum_salary=("salary_mid", "min"),
        maximum_salary=("salary_mid", "max")
    )
    .sort_values(
        "median_salary",
        ascending=False
    )
)


print("\nSalary by job category:")

print(
    category_salary.round(2)
)


# ============================================================
# 6. SAVE CATEGORY SUMMARY
# ============================================================

CATEGORY_OUTPUT = DATA_DIR / "06_salary_by_job_category.csv"

category_salary.round(2).to_csv(
    CATEGORY_OUTPUT,
    index=False
)

# ============================================================
# 7. OVERALL SALARY SUMMARY
# ============================================================

overall_salary = pd.DataFrame({
    "metric": [
        "Total jobs",
        "Jobs with salary",
        "Salary disclosure %",
        "Average salary",
        "Median salary",
        "Minimum salary",
        "Maximum salary"
    ],

    "value": [
        len(df),
        len(salary_jobs),

        round(
            salary_jobs.shape[0]
            / df.shape[0]
            * 100,
            2
        ),

        round(
            salary_jobs["salary_mid"].mean(),
            2
        ),

        round(
            salary_jobs["salary_mid"].median(),
            2
        ),

        round(
            salary_jobs["salary_mid"].min(),
            2
        ),

        round(
            salary_jobs["salary_mid"].max(),
            2
        )
    ]
})


print("\nOverall salary summary:")

print(overall_salary)


# ============================================================
# 8. SAVE
# ============================================================

SUMMARY_OUTPUT = DATA_DIR / "07_salary_summary.csv"

overall_salary.to_csv(
    SUMMARY_OUTPUT,
    index=False
)

print("\nSaved:")
print(CATEGORY_OUTPUT)
print(SUMMARY_OUTPUT)

# ============================================================
# 9. LOW SALARY CHECK
# ============================================================

print("\nSuspiciously low salaries:")

print(
    salary_jobs[
        salary_jobs["salary_mid"] < 100000
    ][
        [
            "title",
            "salary_min",
            "salary_max",
            "salary_mid"
        ]
    ]
    .sort_values("salary_mid")
    .head(30)
    .to_string(index=False)
)