import pytest

from app.strategies.transformers.transform_df_strategy import TransformDF
from app.strategies.extractors.bloomberg_commodity_strategy import BloombergCommodityExtractS
from app.strategies.extractors.usd_cny_currency_strategy import USDCurrencyExtractS
from app.strategies.extractors.chinese_cash_services_strategy import ChineseCashServicesExtractS

import polars as pl
import pandas as pd

@pytest.fixture
def transformer():
    return TransformDF()

@pytest.fixture
def config():
    from app.utils.config import load_config
    return load_config()

def test_transformation(transformer, config):
    df_ex = pl.DataFrame({
        "date": ["2024-05-19", "19/05/2024", "2024/05/19", "May 19, 2024", "2024-05-19T00:00:00", "2678400000"],
        "last": ["1,234.56", "-789,01", "R$ 100,00", "€200.50", "abc123", "99,99"],
        "open": [ "1.200,00", "1,100.50", "R$ 950,00", "€1.000,00", "N/A", "1.000"],
        "high": ["1.250,00", "1,150.75", "R$ 1.050,00", "€1.100,00", "N/A", "1.100"],
        "low": ["1.180,00", "1,080.25", "R$ 900,00", "€950,00", "N/A", "900"],
        "variation": ["+0.3%", "-0.8%", "N/A", "5%", "0%", "+1.2%"],
        "text": ["Café", "ação!", "123", "hello\nworld", "áéíóú", "test"]
    })

    try:
        df_transformed = transformer.transform(df_ex)

    except Exception as e:
        print(e)

    assert isinstance(df_transformed, pd.DataFrame)
    assert list(df_transformed.columns) == list(df_ex.columns)

expected_columns = ['date', 'last', 'open', 'high', 'low', 'variation']

def test_bloomberg_transformation(transformer, config):
    extractor = BloombergCommodityExtractS(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    print(df_transformed.head())
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(expected_columns).issubset(df_transformed.columns)
    assert pd.api.types.is_string_dtype(df_transformed['date'])
    assert pd.api.types.is_float_dtype(df_transformed['last'])
    assert pd.api.types.is_float_dtype(df_transformed['open'])
    assert pd.api.types.is_float_dtype(df_transformed['high'])
    assert pd.api.types.is_float_dtype(df_transformed['low'])
    assert pd.api.types.is_float_dtype(df_transformed['variation'])

def test_usd_currency_transformation(transformer, config):
    extractor = USDCurrencyExtractS(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    print(df_transformed.head())
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(expected_columns).issubset(df_transformed.columns)
    assert pd.api.types.is_string_dtype(df_transformed['date'])
    assert pd.api.types.is_float_dtype(df_transformed['last'])
    assert pd.api.types.is_float_dtype(df_transformed['open'])
    assert pd.api.types.is_float_dtype(df_transformed['high'])
    assert pd.api.types.is_float_dtype(df_transformed['low'])
    assert pd.api.types.is_float_dtype(df_transformed['variation'])

def test_chinese_cash_services_transformation(transformer, config):
    extractor = ChineseCashServicesExtractS(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    print(df_transformed)
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(['date', 'value']).issubset(df_transformed.columns)
    assert pd.api.types.is_string_dtype(df_transformed['date'])
    assert pd.api.types.is_float_dtype(df_transformed['value'])

