

with main_records as (
    select * from {{ source('raw_gbif_birds', 'gbif_bird_occurrences') }}
),

issues_aggregated as (
    select 
        _dlt_parent_id,
        listagg(value, ', ') as issues_list
    from {{ source('raw_gbif_birds', 'gbif_bird_occurrences__issues') }}
    group by _dlt_parent_id
),

renamed as (
    select
        -- Identifiers
        m.gbif_id::varchar as occurrence_key,
        m.dataset_key::varchar as dataset_key,
        m.species_key::varchar as species_key,

        -- Taxonomy
        m.accepted_scientific_name::varchar as accepted_scientific_name,
        m.species::varchar as species_name,
        m.kingdom::varchar as kingdom,
        m.class::varchar as taxon_class,
        m.order_key::varchar as taxon_order,
        m.family::varchar as family,
        m.genus::varchar as genus,
        m.taxon_rank::varchar as taxon_rank,
        m.taxonomic_status::varchar as taxonomic_status,

        -- Location & Dates
        m.event_date::timestamp_tz as event_date,
        m.year::int as year,
        m.month::int as month,
        m.day::int as day,
        m.decimal_latitude::float as decimal_latitude,
        m.decimal_longitude::float as decimal_longitude,
        
        null::float as coordinate_uncertainty_m,
        m.country_code::varchar as country_code,

        -- Status & Joined Issues
        m.basis_of_record::varchar as basis_of_record,
        m.occurrence_status::varchar as occurrence_status,
        coalesce(i.issues_list, '') as issues,
        
        -- Media placeholder
        null::varchar as media_url,
        m.last_interpreted::timestamp_tz as last_interpreted

    from main_records m
    left join issues_aggregated i 
        on m._dlt_id = i._dlt_parent_id
)

select * from renamed

