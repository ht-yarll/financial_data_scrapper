import pytest

from dags.financial_data_scraper.utils.bq_helper import BigQueryHelper
import pandas as pd

bq = BigQueryHelper()

def test_validation_of_bq_credentials():
    result = bq.make_query("SELECT 1 AS test_col")
    rows = list(result)
    assert len(rows) == 1
    assert rows[0].test_col == 1

def test_if_table_is_created_from_df():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })
    table_name = "test_temp_table"

    bq.load_pd_dataframe_on_bq(df, table_name)

    result = bq.make_query(f"SELECT * FROM `{bq.project_id}.{bq.config['services']['bigquery']['dataset']}.{table_name}`")
    rows = list(result)
    assert len(rows) == 3

    bq.bq.delete_table(f"{bq.project_id}.{bq.config['services']['bigquery']['dataset']}.{table_name}", not_found_ok=True)