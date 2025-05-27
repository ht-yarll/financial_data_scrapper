from app.interfaces.extractor_strat_interface import ExtractStrategy
import requests
import polars as pl


class ChineseCashServicesExtract(ExtractStrategy):
    def __init__(self, config):
        self.config = config
        self.url = config['urls']['chinese_pmi']

    def extract(self) -> pl.DataFrame:
        try:
            res = requests.get(self.url)
            results = res.json()
            values = results['candles']
            df = pl.DataFrame(values, schema=['timestamp', 'value'], strict=False)
            df = df.with_columns([
                (pl.col('timestamp').cast(pl.Datetime).dt.cast_time_unit('ms')).alias('date')
            ]).select(['date', 'value']).cast({'date': pl.Utf8, 'value': pl.Utf8})

            print(f'🐻‍❄️ Dataframe Chinese PMI generated with schema: "date", "value"')

            return df
        
        except Exception as e:
            print(f'Failed to create df PMI_Chinese: {e}')
