from csv import DictWriter, QUOTE_ALL

from financial_data_scraper.utils.selenium_helper import SeleniumHelper
from financial_data_scraper.interfaces.extractor_strat_interface import ExtractStrategy

import polars as pl

class USDCurrency(ExtractStrategy):
    def __init__(self, config):
        self.config = config
    
    def extract(self) -> pl.DataFrame:
        try:
            selenium = SeleniumHelper(self.config['urls']['usd_currency'])
            elements = selenium.get_monthly_elements()
            values = []
            for e in elements:
                dolar_dict = {
                    "date": e[0],
                    "value": e[1],
                    "variation": e[2]
                }
                values.append(dolar_dict)

            schema={'date':pl.Utf8, 'value':pl.Utf8, 'variation':pl.Utf8}    
            df = pl.DataFrame(values, schema = schema)
            print(f'🐻‍❄️ Dataframe USD_Currency generated with schema {schema}')
            return df
        
        except Exception as e:
            print(f'Failed to create df USD: {e}')
