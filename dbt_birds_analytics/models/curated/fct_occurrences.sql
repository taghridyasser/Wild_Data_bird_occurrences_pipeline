SELECT
    occurrence_key,
    -- FK
    species_key,
    dataset_key,
    --date
    event_date,
    year,
    month,
    day,
    --location
    decimal_latitude,
    decimal_longitude,
    coordinate_uncertainty_m,
    country_code,
    --record information
    basis_of_record,
    occurrence_status,

    --media
    media_url,
    CASE
        when media_url IS NOT NULL 
            AND TRIM (media_url) != '' 
        THEN TRUE
        ELSE FALSE
    END AS has_media,
    --DATA QUALITY
    issues,
FROM {{ ref('stg_occurrences') }}



