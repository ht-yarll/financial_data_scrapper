from csv import DictWriter, QUOTE_ALL

from financial_data_scraper.interfaces.extractor_strat_interface import ExtractStrategy
import requests
import polars as pl


class ChineseCashServices(ExtractStrategy):
    def __init__(self, config):
        self.config = config
        self.url =' https://sbcharts.investing.com/charts_xml/cce9bf7363d8e7d1609664b9b9e2d468_max.json'

    def extract(self) -> pl.DataFrame:
        res = requests.get(self.url)
        results = res.json()
        values = results['candles']
        df = pl.DataFrame(values, schema=['timestamp', 'value'], strict=False)
        df = df.with_columns([
            (pl.col('timestamp').cast(pl.Datetime).dt.cast_time_unit('ms')).alias('date')
        ]).select(['date', 'value'])
        print(df.head())
        return df
