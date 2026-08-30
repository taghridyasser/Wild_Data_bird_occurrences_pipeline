import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from birds_pipeline import gbif_source , pipeline

@dlt_assets(
    dlt_source=gbif_source(),
    dlt_pipeline=pipeline
)
def gbif_birds_dlt_assets(
    context: dg.AssetExecutionContext,
    dlt: DagsterDltResource,
):
    yield from dlt.run(context=context)