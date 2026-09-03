
FROM python:3.13.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements-docker.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-docker.txt

# Copy DLT + Dagster project
COPY birds_dlt ./birds_dlt

# Copy dbt project
COPY dbt_birds_analytics ./dbt_birds_analytics

# Dagster needs to find the Python package
ENV PYTHONPATH=/app/birds_dlt/src

# Dagster UI
EXPOSE 3000

WORKDIR /app/birds_dlt

# Generate dbt manifest before Dagster starts
CMD ["sh", "-c", "cd /app/dbt_birds_analytics && dbt parse --profiles-dir . && cd /app/birds_dlt && dagster dev -h 0.0.0.0 -p 3000"]

