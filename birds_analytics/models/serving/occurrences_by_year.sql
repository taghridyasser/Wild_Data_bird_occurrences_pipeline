SELECT 
species_key,
year,
COUNT (*) AS occurrence_count
FROM {{ ref('fct_occurrences') }}
GROUP BY 
species_key, 
year