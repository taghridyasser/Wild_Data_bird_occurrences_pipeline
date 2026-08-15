
SELECT 
    OCCURRENCE_ID AS occurrence_key,
    DATASET_ID AS dataset_key,
    LAST_INTERPRETED AS last_interpreted,
    ACCEPTED_SCIENTIFIC_NAME AS accepted_scientific_name,
    SPECIES_ID AS species_key,
    SPECIES AS species_name,
    KINGDOM AS kingdom,
    TAXON_CLASS AS taxon_class,
    TAXON_ORDER AS taxon_order,
    FAMILY AS family,
    GENUS AS genus,
    TAXON_RANK AS taxon_rank,
    TAXONOMIC_STATUS AS taxonomic_status,
    EVENT_DATE AS event_date,
    YEAR AS year,
    MONTH AS month,
    DAY AS day,
    LATITUDE AS decimal_latitude,
    LONGITUDE AS decimal_longitude,
    LOCATION_UNCERTAINTY_M AS coordinate_uncertainty_m,
    COUNTRY_CODE AS country_code,
    RECORD_TYPE AS basis_of_record,
    OCCURRENCE_STATUS AS occurrence_status,
    MEDIA_URL AS media_url,
    ISSUES AS issues
FROM {{ source('raw_data', 'OCCURRENCES') }}

