from pathlib import Path

from dagster import Definitions
from dagster_dlt import DagsterDltResource
from dagster_dbt import DbtCliResource

from birds_dagster.dlt_assets import gbif_birds_dlt_assets
from birds_dagster.dbt_assets import birds_dbt_assets
from birds_dagster.jobs import (
    gbif_daily_job,
    gbif_daily_schedule,
)



DBT_PROJECT_DIR = (
    Path(__file__).resolve().parents[3]
    / "dbt_birds_analytics"
)


defs = Definitions(
    assets=[
        gbif_birds_dlt_assets,
        birds_dbt_assets,
    ],
    
    jobs=[
        gbif_daily_job,
    ],
    schedules=[
        gbif_daily_schedule,
    ],
    resources={
            "dlt": DagsterDltResource(),
            "dbt": DbtCliResource(
                project_dir=DBT_PROJECT_DIR,
                profiles_dir=Path.home() / ".dbt",
            ),
    },
)