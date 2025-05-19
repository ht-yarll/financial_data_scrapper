import pytest
from financial_data_scraper.pipeline.transformers.bq_pattern_transform import PatternBQ
from financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity
from financial_data_scraper.utils.config import load_config

import polars as pl
import pandas as pd
import pandas.testing as pdt


def test_transformation():
    df_ex = pl.DataFrame({
        "date": ["2024-05-19", "19/05/2024", "2024/05/19", "May 19, 2024", "2024-05-19T00:00:00"],
        "value": ["1,234.56", "-789,01", "R$ 100,00", "€200.50", "abc123"],
        "variaiton": ["+0.3%", "-0.8%", "N/A", "5%", "0%"],
        "text": ["Café", "ação!", "123", "hello\nworld", "áéíóú"]
    })
    t = PatternBQ()

    try:
        df_transformed = t.transform(df_ex)

    except Exception as e:
        print(e)

    assert isinstance(df_transformed, pd.DataFrame)
    assert list(df_transformed.columns) == list(df_ex.columns)