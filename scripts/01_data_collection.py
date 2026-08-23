import os
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
import time

# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


# ============================================================
# SETTINGS
# ============================================================

SEARCH_TERMS = [
    "Analyst",
    "Data Analyst",
    "Business Analyst",
    "BI Analyst",
    "Financial Analyst",
    "Product Analyst",
    "MIS Analyst",
    "Risk Analyst",
    "Quality Analyst",
    "Operations Analyst"
]

START_PAGE = 1
MAX_PAGES_PER_SEARCH = 50

RESULTS_PER_PAGE = 100

OUTPUT_FILE = "01_analyst_jobs_master_raw.csv"

WAIT_SECONDS = 3


# ============================================================
# LOAD EXISTING DATA
# ============================================================

all_rows = []
seen_job_ids = set()


if os.path.exists(OUTPUT_FILE):

    existing_df = pd.read_csv(OUTPUT_FILE)

    print("Existing dataset found.")
    print("Existing rows:", len(existing_df))

    if "job_id" in existing_df.columns:

        seen_job_ids.update(
            existing_df["job_id"].dropna().astype(str)
        )

        all_rows = existing_df.to_dict("records")


    else:
     print("No existing master dataset found.")

print("\nExisting unique jobs:", len(seen_job_ids))


# ============================================================
# SCRAPE MULTIPLE SEARCH TERMS
# ============================================================

for search_term in SEARCH_TERMS:

    print("\n" + "=" * 60)
    print("SEARCH:", search_term)
    print("=" * 60)

    for page in range(
        START_PAGE,
        START_PAGE + MAX_PAGES_PER_SEARCH
    ):

        print(f"\nCollecting page {page}...")

        url = (
            "https://api.adzuna.com/"
            f"v1/api/jobs/in/search/{page}"
        )

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": RESULTS_PER_PAGE,
            "what": search_term
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

        except requests.exceptions.RequestException as e:

            print("Request failed:", e)
            print("Moving to next page.")

            continue


        print("Status:", response.status_code)


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if response.status_code == 200:

            data = response.json()

            jobs = data.get("results", [])

            print("Jobs received:", len(jobs))


            if not jobs:

                print("No jobs returned.")
                break


            new_jobs = 0


            for job in jobs:

                job_id = job.get("id")

                if job_id is None:
                    continue


                job_id = str(job_id)


                # ------------------------------------------------
                # REMOVE DUPLICATES ACROSS ALL SEARCH TERMS
                # ------------------------------------------------

                if job_id in seen_job_ids:

                    continue


                seen_job_ids.add(job_id)


                row = {

                    "job_id": job_id,

                    "search_term": search_term,

                    "title":
                        job.get("title"),

                    "company":
                        job.get("company", {})
                        .get("display_name"),

                    "location":
                        job.get("location", {})
                        .get("display_name"),

                    "salary_min":
                        job.get("salary_min"),

                    "salary_max":
                        job.get("salary_max"),

                    "description":
                        job.get("description"),

                    "created":
                        job.get("created")
                }


                all_rows.append(row)

                new_jobs += 1


            print("New unique jobs:", new_jobs)
            print("Total unique jobs:", len(all_rows))


            # ------------------------------------------------
            # SAVE PROGRESS AFTER EVERY PAGE
            # ------------------------------------------------

            pd.DataFrame(all_rows).to_csv(
                OUTPUT_FILE,
                index=False
            )

            print("Progress saved.")


            time.sleep(WAIT_SECONDS)


        # ----------------------------------------------------
        # RATE LIMIT
        # ----------------------------------------------------

        elif response.status_code == 429:

            print("Rate limit reached.")

            print(
                "Stopping safely. "
                "Run the scraper again later."
            )

            break


        # ----------------------------------------------------
        # TEMPORARY SERVER ERROR
        # ----------------------------------------------------

        elif response.status_code == 503:

            print("Server temporarily unavailable.")

            print("Waiting 10 seconds before continuing.")

            time.sleep(10)

            continue


        # ----------------------------------------------------
        # AUTHENTICATION
        # ----------------------------------------------------

        elif response.status_code == 401:

            print("401 Unauthorized.")

            print(
                "Check your APP_ID and APP_KEY."
            )

            break


        # ----------------------------------------------------
        # OTHER ERROR
        # ----------------------------------------------------

        else:

            print(
                "Request failed with status:",
                response.status_code
            )

            print(response.text[:500])

            break


# ============================================================
# FINAL OUTPUT
# ============================================================

df = pd.DataFrame(all_rows)


print("\n" + "=" * 60)
print("FINAL COLLECTION")
print("=" * 60)

print("Rows:", len(df))

print("Columns:", len(df.columns))


if "job_id" in df.columns:

    print(
        "Unique job IDs:",
        df["job_id"].nunique()
    )

    print(
        "Duplicate job IDs:",
        df["job_id"].duplicated().sum()
    )


print("\nSearch term distribution:")

if "search_term" in df.columns:

    print(
        df["search_term"].value_counts()
    )


df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nFinal dataset saved:")
print(OUTPUT_FILE)