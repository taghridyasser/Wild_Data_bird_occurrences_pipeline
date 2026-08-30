

"""
GBIF Birds dlt Pipeline — Snowflake Destination
================================================
Extracts bird occurrence records from the GBIF Occurrence Search API
and loads them into Snowflake.

Scope:
  - Endpoint : GET https://api.gbif.org/v1/occurrence/search
  - Country  : CH  (Switzerland, ISO 3166-1 alpha-2)
  - Year     : 2015 onward  (year=2015,2026 — GBIF range syntax)
  - Taxon    : classKey=212  (Aves — GBIF backbone key for birds)
  - Limit    : 1 000 records for this initial load

Run:
  pip install "dlt[snowflake]" requests python-dotenv
  python birds_pipeline.py
"""

import os
import dlt
import requests
from typing import Iterator
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# ──────────────────────────────────────────────
# GBIF API Config
# ──────────────────────────────────────────────
GBIF_BASE_URL  = "https://api.gbif.org/v1/occurrence/search"
COUNTRY        = "CH"           # Switzerland
YEAR   = "2015"    # 2015 onward (GBIF range: "min,max")
CLASS_KEY      = 212            # Aves (birds) — numeric key required
PAGE_SIZE      = 300            # GBIF hard cap per page
TARGET_RECORDS = int(os.getenv("TARGET_RECORDS", 1_000))


# ──────────────────────────────────────────────
# Snowflake Credentials (loaded from .env)
# ──────────────────────────────────────────────
#

# ──────────────────────────────────────────────
# dlt resource — paginates GBIF
# ──────────────────────────────────────────────
@dlt.resource(
    name="gbif_bird_occurrences",
    write_disposition="replace",  # full refresh each run
    primary_key="gbifID",
)
def gbif_bird_occurrences() -> Iterator[dict]:
    """
    Pages through GBIF Occurrence Search and yields one dict per record.

    ⚠️  classKey=212 is required — the API silently ignores class=Aves (text).
    """
    headers = {"User-Agent": "wwf-dlt-pipeline/1.0 (contact@wwf.ch)"}
    fetched, offset = 0, 0

    while fetched < TARGET_RECORDS:
        batch  = min(PAGE_SIZE, TARGET_RECORDS - fetched)
        params = {
            "country"  : COUNTRY,
            "year"     : YEAR,
            "classKey" : CLASS_KEY,
            "limit"    : batch,
            "offset"   : offset,
        }

        response = requests.get(GBIF_BASE_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        payload  = response.json()
        results  = payload.get("results", [])

        if not results:
            break

        for record in results:
            yield _flatten_record(record)

        fetched += len(results)
        offset  += len(results)

        if payload.get("endOfRecords", True):
            break

    print(f"[gbif_birds] Done — {fetched} records yielded.")


def _flatten_record(record: dict) -> dict:
    """Remove heavy nested fields GBIF returns that we don't need."""
    for key in (
        "classifications", "networkKeys", "extensions",
        "facts", "relations", "media", "identifiers",
        "dnaSequenceID", "nucleotideSequence",
        "recordedByIDs", "identifiedByIDs",
    ):
        record.pop(key, None)
    return record


# ──────────────────────────────────────────────
# dlt source
# ──────────────────────────────────────────────
@dlt.source(name="gbif")
def gbif_source():
    return gbif_bird_occurrences()


# ──────────────────────────────────────────────
# Pipeline entry point
# ──────────────────────────────────────────────


pipeline = dlt.pipeline(
    pipeline_name="gbif_birds_ch",
    destination="snowflake",
    dataset_name="raw_gbif_birds",
)


if __name__ == "__main__":

    print("Starting pipeline run...")
    load_info = pipeline.run(gbif_source())

    print(load_info)
    print("Done!Check Snowflake → database: birds_dlt_db → table: gbif_bird_occurrences")