import pytest
from dags.financial_data_scraper.utils.config import load_config
from dags.financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity
from dags.financial_data_scraper.pipeline.extractors.chinese_cash_services import ChineseCashServices
from dags.financial_data_scraper.pipeline.extractors.usd_currency import USDCurrency

import polars as pl

config = load_config()

def test_bloomberg_returns_valid_dataframe():
    bloom = BloombergCommodity(config)
    df = bloom.extract()
    df = df.head()

    expected = {
        'date':pl.Utf8, 'value':pl.Utf8, 'variation':pl.Utf8
    }

    assert isinstance(df, pl.DataFrame)
    for col, dtype in expected.items():
        assert col in df.schema
        assert df.schema[col] == dtype


def test_usd_currency_returns_valid_dataframe():
    usd = USDCurrency(config)
    df = usd.extract()
    df = df.head()

    expected = {
        'date':pl.Utf8, 'value':pl.Utf8, 'variation':pl.Utf8
    }

    assert isinstance(df, pl.DataFrame)
    for col, dtype in expected.items():
        assert col in df.schema
        assert df.schema[col] == dtype


def test_chinese_cash_services_returns_valid_dataframe():
    chin = ChineseCashServices(config)
    df = chin.extract()
    df = df.head()
    print(df)

    expected = {
        'date': pl.Utf8, 
        'value': pl.Utf8
    }

    assert isinstance(df, pl.DataFrame)
    for col in expected:
        assert col in df.schema
