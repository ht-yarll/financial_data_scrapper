from app.context.etl import extract_transform_load
from app.utils.config import load_config
from app.strategies.extractors.bloomberg_commodity_strategy import BloombergCommodityExtract
from app.strategies.extractors.usd_cny_currency_strategy import USDCurrencyExtract
from app.strategies.extractors.chinese_cash_services_strategy import ChineseCashServicesExtract
from app.strategies.transformers.transform_df_strategy import TransformDF
from app.strategies.loaders.loading_to_bq_strategy import BatchDataOnBQ

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    config = load_config()
    
    bloomberg = extract_transform_load( 
        config,
        extractor=BloombergCommodityExtract,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='bloomberg_commodity_extraction'
    )

    usd = extract_transform_load(
        config,
        extractor=USDCurrencyExtract,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='usd_cny_currency_history'
    )

    chinese = extract_transform_load(
        config,
        extractor=ChineseCashServicesExtract,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='chinese_pmi_history'
    )

    return {"status": "ok", "details": ["bloomberg", "usd_cny", "chinese_pmi"]}