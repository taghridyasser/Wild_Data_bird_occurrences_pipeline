# Wild Data – GBIF Bird Occurrences ETL Pipeline

## Project Overview

This project retrieves bird occurrence records from the GBIF (Global Biodiversity Information Facility) API for Switzerland from 2015 onward.

The pipeline downloads occurrence records, stores the raw API responses as JSON files, transforms the data into a clean tabular format using pandas, and exports the final dataset as a CSV file.

An analysis notebook is also included to answer several exploratory questions about the dataset.

---

## Data Source

- GBIF Occurrence API
- Endpoint: `/occurrence/search`
- Documentation: https://techdocs.gbif.org/en/openapi/

Query filters:

- Country: Switzerland (`CH`)
- Taxon: Birds (`taxonKey=212`)
- Years: 2015 onward

---

## Project Structure

```
bird-occurrences/
│
├── data/
│   ├── raw/              # Raw JSON pages downloaded from GBIF
│   └── csv/              # Final cleaned CSV
│
├── notebooks/
│   └── analysis.ipynb    # Exploratory analysis
│
├── src/
│   └── main.py           # ETL pipeline
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/taghridyasser/Wild_Data_bird-occurrences.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

Run the ETL pipeline

```bash
python src/main.py
```

The script will

- Download bird occurrence records from GBIF
- Save each API page as JSON in `data/raw/`
- Combine all downloaded records
- Flatten the `media` field into a single `media_url`
- Keep the required fields
- Rename columns
- Export the cleaned dataset to

```
data/csv/birds_occurrences.csv
```

---

## Output

### Raw Data

```
data/raw/*.json
```

### Clean Dataset

```
data/csv/birds_occurrences.csv
```

---

## Analysis

The notebook `notebooks/analysis.ipynb` answers:

- Top 20 bird species
- Number of occurrences per year
- Number of records without species identification

---

## Technologies

- Python
- Requests
- Pandas
- Jupyter Notebook
- Git
- GitHub

---

## Author

Taghrid Yasser
