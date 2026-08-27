with species_deduplicated AS (
    SELECT
    species_key,
    accepted_scientific_name,
    species_name,
    kingdom,
    taxon_class,
    taxon_order,
    family,
    genus,
    taxon_rank,
    taxonomic_status,
    ROW_NUMBER() OVER (
        PARTITION BY species_key
        ORDER BY accepted_scientific_name  )
        AS row_num
    FROM {{ ref('stg_occurrences') }}
)
 SELECT
    species_key,
    accepted_scientific_name,
    species_name,
    kingdom,
    taxon_class,
    taxon_order,
    family,
    genus,
    taxon_rank,
    taxonomic_status,
FROM species_deduplicated
WHERE row_num = 1