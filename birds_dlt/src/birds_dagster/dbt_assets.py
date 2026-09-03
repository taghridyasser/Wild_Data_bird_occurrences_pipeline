from pathlib import Path

import dagster as dg
from dagster_dbt import (
    DagsterDbtTranslator,
    DbtProject,
    DbtCliResource,
    dbt_assets,
)


DBT_PROJECT_DIR = (
    Path(__file__).resolve().parents[3]
    / "dbt_birds_analytics"
)


class BirdsDbtTranslator(DagsterDbtTranslator):

    def get_asset_spec(self, manifest, unique_id, project):
        spec = super().get_asset_spec(
            manifest,
            unique_id,
            project,
        )

        if unique_id == "model.birds_analytics.stg_occurrences":
            return spec.replace_attributes(
                deps=[
                    *spec.deps,
                    dg.AssetDep(
                        dg.AssetKey(
                            "dlt_gbif_gbif_bird_occurrences"
                        )
                    ),
                ],
            )

        return spec


dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=BirdsDbtTranslator(),
)
def birds_dbt_assets(
    context: dg.AssetExecutionContext,
    dbt: DbtCliResource,
):
    yield from dbt.cli(
        ["build"],
        context=context,
    ).stream()