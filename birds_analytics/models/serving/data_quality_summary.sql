WITH flattened_issues AS (

    SELECT
        TRIM(
            REPLACE(
                REPLACE(
                    value::STRING,
                    '''',
                    ''
                ),
                '"',
                ''
            )
        ) AS issue_flag

    FROM {{ ref('fct_occurrences') }},
    LATERAL FLATTEN(
        INPUT => SPLIT(
            REPLACE(
                REPLACE(issues, '[', ''),
                ']', ''
            ),
            ','
        )
    )

),

issue_counts AS (

    SELECT
        issue_flag,
        COUNT(*) AS record_count

    FROM flattened_issues

    WHERE issue_flag IS NOT NULL
      AND issue_flag != ''

    GROUP BY issue_flag

),

total_records AS (

    SELECT COUNT(*) AS total_count
    FROM {{ ref('fct_occurrences') }}

)

SELECT
    issue_flag,
    record_count,
    ROUND(
        record_count * 100.0 / total_count,
        2
    ) AS pct_of_total

FROM issue_counts
CROSS JOIN total_records