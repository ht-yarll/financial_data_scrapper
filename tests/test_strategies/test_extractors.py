import pytest
from app.utils.config import load_config
from app.strategies.extractors.bloomberg_commodity_strategy import BloombergCommodityExtract
from app.strategies.extractors.chinese_cash_services_strategy import ChineseCashServicesExtract
from app.strategies.extractors.usd_cny_currency_strategy import USDCurrencyExtract

import polars as pl

config = load_config()

expected = {
    'date':pl.Utf8, 'last':pl.Utf8, 'open':pl.Utf8, 'high':pl.Utf8, 'low':pl.Utf8 , 'variation':pl.Utf8
}

def test_bloomberg_returns_valid_dataframe():
    bloom = BloombergCommodityExtract(config)
    df = bloom.extract()
    df = df.head()
    print(df)

    expected_bloom = expected

    assert isinstance(df, pl.DataFrame)
    for col, dtype in expected_bloom.items():
        assert col in df.schema
        assert df.schema[col] == dtype


def test_usd_currency_returns_valid_dataframe():
    usd = USDCurrencyExtract(config)
    df = usd.extract()
    df = df.head()
    print(df)

    expected_usd_cny = expected

    assert isinstance(df, pl.DataFrame)
    for col, dtype in expected_usd_cny.items():
        assert col in df.schema
        assert df.schema[col] == dtype


def test_chinese_cash_services_returns_valid_dataframe():
    chin = ChineseCashServicesExtract(config)
    df = chin.extract()
    df = df.head()
    print(df)

    expected_pmi = {
        'date': pl.Utf8, 
        'value': pl.Utf8
    }

    assert isinstance(df, pl.DataFrame)
    for col in expected_pmi:
        assert col in df.schema
