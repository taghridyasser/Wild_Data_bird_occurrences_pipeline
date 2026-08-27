
```markdown
# Wild Data – GBIF Bird Occurrences & Analytics Pipeline

## Project Overview

This repository contains an end-to-end data pipeline and analytics project for bird occurrence records in Switzerland from 2015 onward, sourced from the GBIF (Global Biodiversity Information Facility) API.

The project handles raw data extraction (Python / dlt), storage and warehousing (Snowflake), and data transformation & modeling (dbt).

---

## Data Source

- **GBIF Occurrence API**: `/occurrence/search`
- **Documentation**: [https://techdocs.gbif.org/en/openapi/](https://techdocs.gbif.org/en/openapi/)
- **Filters**:
  - Country: Switzerland (`CH`)
  - Class: Birds (`classKey=212`)
  - Years: 2015 onward

---

## Architecture & Data Layers

Data flows through three main layers inside Snowflake managed via dbt:


```

RAW (dlt / CSV) ──> CURATED (dbt Staging & Dims) ──> SERVING (dbt Analytics)

```

### 1. Raw Layer
- JSON responses and dlt pipelines landing raw records directly into Snowflake (`raw_gbif_birds`).

### 2. Curated Layer (dbt)
- `stg_occurrences`: Standardizes, casts types, and flattens fields.
- `dim_species`: Deduplicated species metadata.
- `dim_dataset`: Dataset lineage and metrics.
- `fct_occurrences`: Core fact table linking occurrences to dimensions.

### 3. Serving Layer (dbt)
- `species_occurrence_summary`: Aggregated metrics per species.
- `occurrences_by_year`: Yearly observation counts per species.
- `data_quality_summary`: Quality issue breakdowns and coverage.

---

## Project Structure

```text
bird-occurrences/
├── data/
│   ├── raw/                  # Downloaded GBIF JSON responses
│   └── csv/                  # Cleaned CSV exports
├── dbt_birds_analytics/       # dbt Project
│   ├── models/
│   │   ├── curated/          # Staging, Dim, and Fact SQL models
│   │   └── serving/          # Final reporting models
│   ├── dbt_project.yml
│   └── profiles.yml
├── notebooks/
│   └── analysis.ipynb        # Exploratory analysis
├── src/
│   └── main.py               # Python extraction scripts
├── README.md
├── requirements.txt
└── .gitignore

```

---

## Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/taghridyasser/Wild_Data_bird-occurrences.git](https://github.com/taghridyasser/Wild_Data_bird-occurrences.git)
cd Wild_Data_bird-occurrences

```


2. **Set up Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```


3. **Run dbt Transformations:**
```bash
cd dbt_birds_analytics
dbt run
dbt test

```



---

## Technologies Used

* **Python, Pandas, Requests** (ETL & Analysis)
* **dlt** (Automated pipeline loading)
* **Snowflake** (Cloud Data Warehouse)
* **dbt (data build tool)** (Data Transformations & Data Quality)
* **SQL, Git, GitHub**

---

## Author

**Taghrid Yasser**

