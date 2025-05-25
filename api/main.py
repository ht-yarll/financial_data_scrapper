from api.context.etl import extract_transform_load
from api.utils.config import load_config
from api.pipeline.extractors.bloomberg_commodity import BloombergCommodityExtract
from api.pipeline.extractors.usd_currency import USDCurrencyExtract
from api.pipeline.extractors.chinese_cash_services import ChineseCashServicesExtract
from api.pipeline.transformers.transforms_df import TransformDF
from api.pipeline.loaders.loading_to_bq import BatchDataOnBQ

from flask import Flask

app = Flask(__name__)

@app.route("/")
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
        table_name='usd_currency_history'
    )

    chinese = extract_transform_load(
        config,
        extractor=ChineseCashServicesExtract,
        transformer=TransformDF,
        loader=BatchDataOnBQ,
        table_name='chinese_pmi_history'
    )

    bloomberg
    usd
    chinese


if __name__ == "__main__":
    app.dep