import pytest

from app.pipeline.transformers.transforms_df import TransformDF
from app.pipeline.extractors.bloomberg_commodity import BloombergCommodityExtract
from app.pipeline.extractors.usd_currency import USDCurrencyExtract
from app.pipeline.extractors.chinese_cash_services import ChineseCashServicesExtract

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
        "date": ["2024-05-19", "19/05/2024", "2024/05/19", "May 19, 2024", "2024-05-19T00:00:00"],
        "value": ["1,234.56", "-789,01", "R$ 100,00", "€200.50", "abc123"],
        "variation": ["+0.3%", "-0.8%", "N/A", "5%", "0%"],
        "text": ["Café", "ação!", "123", "hello\nworld", "áéíóú"]
    })

    try:
        df_transformed = transformer.transform(df_ex)

    except Exception as e:
        print(e)

    assert isinstance(df_transformed, pd.DataFrame)
    assert list(df_transformed.columns) == list(df_ex.columns)

def test_bloomberg_transformation(transformer, config):
    extractor = BloombergCommodityExtract(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(['date', 'value', 'variation']).issubset(df_transformed.columns)
    assert pd.app.types.is_datetime64_any_dtype(df_transformed['date'])
    assert pd.app.types.is_float_dtype(df_transformed['value'])
    assert pd.app.types.is_float_dtype(df_transformed['variation'])

def test_usd_currency_transformation(transformer, config):
    extractor = USDCurrencyExtract(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(['date', 'value', 'variation']).issubset(df_transformed.columns)
    assert pd.app.types.is_datetime64_any_dtype(df_transformed['date'])
    assert pd.app.types.is_float_dtype(df_transformed['value'])
    assert pd.app.types.is_float_dtype(df_transformed['variation'])

def test_chinese_cash_services_transformation(transformer, config):
    extractor = ChineseCashServicesExtract(config)
    df = extractor.extract()
    df_transformed = transformer.transform(df)
    assert isinstance(df_transformed, pd.DataFrame)
    assert set(['date', 'value']).issubset(df_transformed.columns)
    assert pd.app.types.is_datetime64_any_dtype(df_transformed['date'])
    assert pd.app.types.is_float_dtype(df_transformed['value'])

