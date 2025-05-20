import pytest

from financial_data_scraper.utils.bq_helper import BigQueryHelper

bq = BigQueryHelper()

def test_validation_of_bq_credentials():
    result = bq.make_query("SELECT 1 AS test_col")
    rows = list(result)
    assert len(rows) == 1
    assert rows[0].test_col == 1