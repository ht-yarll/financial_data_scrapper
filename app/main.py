from app.context.etl import extract_transform_load
from app.utils.config import load_config
from app.pipeline.extractors.bloomberg_commodity import BloombergCommodityExtract
from app.pipeline.extractors.usd_cny_currency import USDCurrencyExtract
from app.pipeline.extractors.chinese_cash_services import ChineseCashServicesExtract
from app.pipeline.transformers.transforms_df import TransformDF
from app.pipeline.loaders.loading_to_bq import BatchDataOnBQ

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