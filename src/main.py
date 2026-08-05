import json
import requests
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
URL = "https://api.gbif.org/v1/occurrence/search"

TARGET_RECORDS = 1000
LIMIT = 300

offset = 0
downloaded = 0
page = 1

while downloaded < TARGET_RECORDS:

    limit = min(LIMIT, TARGET_RECORDS - downloaded)

    params = {
        "country": "CH",
        "year": "2015",
       #"taxonKey": 212,   # Birds
        "classKey": 212,   # Birds
        "limit": limit,
        "offset": offset
    }

    response = requests.get(URL, params=params)
    response.raise_for_status()

    data = response.json()

    # Save the entire API response

    output_file = RAW_DIR / f"birds_page_{page}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {output_file}")

    downloaded += len(data["results"])

    # Stop if GBIF says there are no more records
    if data["endOfRecords"]:
        print("Reached end of records.")
        break

    offset += limit
    page += 1

# saving the page sat one JSON  file, we can now load all the records into a single list
records = []

for file in sorted(RAW_DIR.glob("*.json")):

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    records.extend(data["results"])

print(f"Loaded {len(records)} records")


#select the fields we want to keep in the final DataFrame
FIELDS = ["key", "datasetKey", "lastInterpreted",
 "acceptedScientificName","speciesKey", "species",
 "kingdom", "class", "order", "family", "genus",
 "taxonRank", "taxonomicStatus",
 "eventDate", "year", "month", "day",
 "decimalLatitude", "decimalLongitude",
 "coordinateUncertaintyInMeters", "countryCode",
 "basisOfRecord", "occurrenceStatus", "issues" , "media",
]

# Create a DataFrame from the list of records and keep only the fields we want
df = pd.json_normalize(records)

# Ensure all required fields exist
for col in FIELDS:
    if col not in df.columns:
        df[col] = None

# Keep only the required fields
df = df[FIELDS].copy()


    
def get_media_url(media):
    """
        Return the identifier of the first media item.
        Return None if there is no media.
        """
    if isinstance(media, list) and len(media) > 0:
        return media[0].get("identifier", "")
    return ""


df["media_url"] = df["media"].apply(get_media_url)


# Drop the original "media" column since we now have a separate "media_url" column
df = df.drop(columns=["media"])


print(df.head())

# Rename the columns to match the desired output format

df.rename(columns={
    "key":"occurrence_id",
    "datasetKey": "dataset_id",
    "lastInterpreted": "last_interpreted",
    "acceptedScientificName": "accepted_scientific_name",
    "speciesKey": "species_id", 
    "species": "species","kingdom": "kingdom", 
    "class": "class", 
    "order": "order", 
    "family": "family", 
    "genus": "genus",
    "taxonRank":"taxon_rank", 
    "taxonomicStatus":"taxonomic_status",
    "eventDate": "event_date", 
    "year": "year",
    "month": "month",
    "day": "day",
    "decimalLatitude": "latitude", 
    "decimalLongitude": "longitude",
    "coordinateUncertaintyInMeters": "location_uncertainty_m", 
    "countryCode": "country_code",
    "basisOfRecord": "record_type", 
    "occurrenceStatus":"occurrence_status", 
    "issues": "issues",
    "media_url": "media_url",
}, inplace=True)



df.to_csv("data/csv/birds_occurrences.csv", index=False)

print(f"Successfully saved {len(df)} records to data/csv/birds_occurrences.csv")