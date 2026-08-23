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
# LOAD DATA
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

INPUT_FILE = DATA_DIR / "01_analyst_jobs_master_raw.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("JOB CLASSIFICATION")
print("=" * 60)

print("\nOriginal rows:", len(df))


# ============================================================
# CLEAN TITLE FOR CLASSIFICATION
# ============================================================

df["title_clean"] = (
    df["title"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
)


# ============================================================
# CLASSIFICATION FUNCTION
# ============================================================

import re

def classify_job(title):

    title = str(title).lower().strip()


    # ========================================================
    # DATA ANALYST
    # ========================================================

    if re.search(r"\bdata analyst\b", title):
        return "Data Analyst"


    # ========================================================
    # BUSINESS ANALYST
    # ========================================================

    if "business analyst" in title:
        return "Business Analyst"


    # ========================================================
    # BI / REPORTING / MIS
    # ========================================================

    if any(keyword in title for keyword in [
        "business intelligence analyst",
        "bi analyst",
        "reporting analyst",
        "mis analyst",
        "analytics analyst",
        "analytics & modeling analyst",
        "analytics and modeling analyst"
    ]):
        return "BI / Reporting / MIS"


    # ========================================================
    # PRODUCT
    # ========================================================

    if "product analyst" in title:
        return "Product Analyst"


    # ========================================================
    # FINANCE / ACCOUNTING
    # ========================================================

    finance_keywords = [
        "financial analyst",
        "finance analyst",
        "fp&a",
        "fp&a analyst",
        "tax analyst",
        "treasury analyst",
        "credit analyst",
        "revenue analyst",
        "pricing analyst",
        "r2r analyst",
        "record to report",
        "accounts payable analyst",
        "accounts receivable analyst",
        "order to cash analyst",
        "procurement analyst"
    ]

    if any(keyword in title for keyword in finance_keywords):
        return "Finance / Accounting Analyst"


    # ========================================================
    # RISK / COMPLIANCE
    # ========================================================

    risk_keywords = [
        "risk analyst",
        "compliance analyst",
        "regulatory analyst",
        "regulatory compliance analyst",
        "credit risk analyst",
        "fraud analyst",
        "security analyst",
        "information security analyst",
        "soc analyst"
    ]

    if any(keyword in title for keyword in risk_keywords):
        return "Risk / Compliance Analyst"


    # ========================================================
    # OPERATIONS / SUPPLY CHAIN
    # ========================================================

    operations_keywords = [
        "operations analyst",
        "operation analyst",
        "procurement analyst",
        "supply chain analyst",
        "inventory analyst",
        "logistics analyst",
        "delivery operations analyst",
        "banking operations analyst",
        "sales operations analyst"
    ]

    if any(keyword in title for keyword in operations_keywords):
        return "Operations / Supply Chain Analyst"


    # ========================================================
    # QUALITY / TESTING
    # ========================================================

    quality_keywords = [
        "quality analyst",
        "quality assurance analyst",
        "qa analyst",
        "quality control analyst",
        "test analyst",
        "testing analyst"
    ]

    if any(keyword in title for keyword in quality_keywords):
        return "Quality / Testing Analyst"


    # ========================================================
    # IT / SYSTEMS
    # ========================================================

    it_keywords = [
        "system analyst",
        "systems analyst",
        "it analyst",
        "technical analyst",
        "service desk analyst",
        "technical support analyst",
        "infrastructure change analyst",
        "maconomy support analyst",
        "product support analyst"
    ]

    if any(keyword in title for keyword in it_keywords):
        return "IT / Systems Analyst"


    # ========================================================
    # SALES / MARKETING
    # ========================================================

    sales_marketing_keywords = [
        "sales analyst",
        "marketing analyst",
        "seo analyst",
        "digital marketing analyst",
        "sales operations analyst",
        "presales analyst",
        "customer success analyst"
    ]

    if any(keyword in title for keyword in sales_marketing_keywords):
        return "Sales / Marketing Analyst"


    # ========================================================
    # HR / PEOPLE
    # ========================================================

    hr_keywords = [
        "hr analyst",
        "human resources analyst",
        "people analyst",
        "workforce analyst",
        "talent analyst",
        "compensation analyst"
    ]

    if any(keyword in title for keyword in hr_keywords):
        return "HR / People Analyst"


    # ========================================================
    # RESEARCH
    # ========================================================

    research_keywords = [
        "research analyst",
        "market research analyst"
    ]

    if any(keyword in title for keyword in research_keywords):
        return "Research Analyst"


    # ========================================================
    # ADJACENT DATA / TECH ROLES
    # ========================================================

    adjacent_tech_keywords = [
        "data engineer",
        "data scientist",
        "data qa",
        "data specialist",
        "machine learning",
        "software engineer",
        "software developer",
        "developer",
        "fullstack",
        "full stack",
        "java developer",
        "salesforce developer",
        "product owner",
        "product manager",
        "project manager"
    ]

    if any(keyword in title for keyword in adjacent_tech_keywords):
        return "Adjacent Data / Tech Role"


    # ========================================================
    # GENERIC ANALYST
    # ========================================================

    if "analyst" in title:
        return "Other Analyst"


    # ========================================================
    # NON-ANALYST
    # ========================================================

    return "Non-Analyst Role"


# ============================================================
# APPLY CLASSIFICATION
# ============================================================

df["job_category"] = df["title"].apply(
    classify_job
)


# ============================================================
# CHECK RESULTS
# ============================================================

print("\nJob categories:")

print(
    df["job_category"]
    .value_counts()
)


print("\nCategory percentages:")

print(
    (
        df["job_category"]
        .value_counts(normalize=True)
        * 100
    ).round(2)
)


# ============================================================
# INSPECT EXAMPLES
# ============================================================

print("\nExample classifications:")

print(
    df[
        [
            "title",
            "job_category"
        ]
    ]
    .drop_duplicates()
    .head(50)
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE = DATA_DIR / "02_analyst_jobs_classified.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "\nSaved:",
    OUTPUT_FILE
)