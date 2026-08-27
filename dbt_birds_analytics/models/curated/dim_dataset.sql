SELECT dataset_key,
    COUNT(*) AS record_count,
    MIN(event_date) AS first_seen, 
    MAX(event_date) AS last_seen
FROM {{ ref('stg_occurrences') }}
GROUP BY dataset_key