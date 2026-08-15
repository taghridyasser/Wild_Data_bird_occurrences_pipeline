SELECT 
    species_key,
    COUNT(*) AS occurrence_count,

    MIN(event_date) AS first_observed, 

    MAX(event_date) AS last_observed,
    COUNT(DISTINCT dataset_key) AS dataset_count,

     ROUND(
        COUNT_IF(
            decimal_latitude IS NOT NULL
            AND decimal_longitude IS NOT NULL
        ) * 100.0 / COUNT(*),
        2
    ) AS pct_with_coordinates

FROM {{ ref('fct_occurrences') }}

GROUP BY species_key
