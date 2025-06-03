from app.context.etl import ExtractTransformLoad
from app.utils.config import load_config
from app.strategies.extractors.bloomberg_commodity_strategy import BloombergCommodityExtractS
from app.strategies.extractors.usd_cny_currency_strategy import USDCurrencyExtractS
from app.strategies.extractors.chinese_cash_services_strategy import ChineseCashServicesExtractS
from app.strategies.transformers.transform_df_strategy import TransformDF
from app.strategies.loaders.loading_to_bq_strategy import BatchDataOnBQ

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    config = load_config()
    
    bloomberg_etl = ExtractTransformLoad( 
        config,
        extractor=BloombergCommodityExtractS,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='bloomberg_commodity_extraction'
    )
    bloomberg_etl.run()

    usd_cny_etl = ExtractTransformLoad(
        config,
        extractor=USDCurrencyExtractS,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='usd_cny_currency_history'
    )
    usd_cny_etl.run()

    chinese_pmi_etl = ExtractTransformLoad(
        config,
        extractor=ChineseCashServicesExtractS,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='chinese_pmi_history'
    )
    chinese_pmi_etl.run()

    return {"status": "ok", "details": ["bloomberg", "usd_cny", "chinese_pmi"]}