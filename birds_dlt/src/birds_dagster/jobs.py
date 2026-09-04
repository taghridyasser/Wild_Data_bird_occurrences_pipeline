import dagster as dg

gbif_daily_job = dg.define_asset_job(
    name="gbif_daily_job",
    selection=dg.AssetSelection.all(),
)

gbif_daily_schedule = dg.ScheduleDefinition(
    name="gbif_daily_schedule",
    job=gbif_daily_job,
    cron_schedule="0 0 * * *",
)