import pytest
from api.utils.config import load_config
from api.pipeline.extractors.bloomberg_commodity import BloombergCommodityExtract
from api.pipeline.extractors.chinese_cash_services import ChineseCashServicesExtract
from api.pipeline.extractors.usd_currency import USDCurrencyExtract

import polars as pl

config = load_config()

def test_bloomberg_returns_valid_dataframe():
    bloom = BloombergCommodityExtract(config)
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
    usd = USDCurrencyExtract(config)
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
    chin = ChineseCashServicesExtract(config)
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
