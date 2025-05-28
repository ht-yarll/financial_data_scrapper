from app.utils.selenium_helper import SeleniumHelper
from app.interfaces.extractor_strat_interface import ExtractStrategy

import polars as pl

class USDCurrencyExtract(ExtractStrategy):
    def __init__(self, config):
        self.config = config
    
    def extract(self) -> pl.DataFrame:
        try:
            selenium = SeleniumHelper(self.config['urls']['usd_currency'])
            elements = selenium.get_monthly_elements()
            schema={'date':pl.Utf8, 'last':pl.Utf8, 'open':pl.Utf8, 'high':pl.Utf8, 'low':pl.Utf8 , 'variation':pl.Utf8}    
            df = pl.DataFrame(elements, schema = schema)
            print(f'🐻‍❄️ Dataframe USD_CNY_Currency generated with schema {schema}')
            selenium.quit_session()
            
            return df
        
        except Exception as e:
            print(f'Failed to create df USD: {e}')
