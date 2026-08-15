# Birds Analytics - dbt Project

This project uses dbt and Snowflake to transform GBIF bird occurrence data
into analytics-ready datasets.

## Architecture

The dbt project follows a layered data transformation approach:

RAW
↓
CURATED
↓
SERVING

### Curated Layer

#### stg_occurrences
Standardizes and cleans the raw occurrence data.

#### dim_species
One row per species.

Columns:
- species_key
- accepted_scientific_name
- species
- kingdom
- taxon_class
- taxon_order
- family
- genus
- taxon_rank
- taxonomic_status

#### dim_dataset
One row per dataset.

Columns:
- dataset_key
- record_count
- first_seen
- last_seen

#### fct_occurrences
One row per occurrence.

Contains:
- occurrence_key
- species_key
- dataset_key
- event_date
- year
- month
- day
- decimal_latitude
- decimal_longitude
- coordinate_uncertainty_m
- country_code
- basis_of_record
- occurrence_status
- media_url
- has_media
- issues

## Serving Layer

### species_occurrence_summary
One row per species.

Provides:
- occurrence_count
- first_observed
- last_observed
- dataset_count
- pct_with_coordinates

### occurrences_by_year
One row per species × year.

Provides:
- occurrence_count

### data_quality_summary
One row per issue flag.

Provides:
- record_count
- pct_of_total

## Data Source

The data comes from the GBIF occurrence API.

The dataset contains 1,000 bird occurrence records collected for Switzerland
from 2015 onward.

## Technologies

- Python
- GBIF API
- Snowflake
- dbt
- SQL
- Git / GitHub

## Validation

The dbt project was validated using:

```bash
dbt parse
dbt build
