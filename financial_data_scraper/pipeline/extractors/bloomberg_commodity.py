from financial_data_scraper.utils.selenium_helper import SeleniumHelper
from financial_data_scraper.interfaces.extractor_strat_interface import ExtractStrategy

import polars as pl

class BloombergCommodity(ExtractStrategy):
    def __init__(self, config):
        self.config = config
    
    def extract(self) -> pl.DataFrame:
        try:
            selenium = SeleniumHelper(self.config['urls']['commodity'])
            elements = selenium.get_monthly_elements()
            values = []
            for e in elements:
                bloomberg_dict = {
                    "date": e[0],
                    "value": e[1],
                    "variation": e[2]
                }
                values.append(bloomberg_dict)
            schema = ['date', 'value', 'variation']
            df = pl.DataFrame(values, schema = schema)
            print(f'🐻‍❄️ Dataframe Bloomberg_Commodity generated with schema {schema}')
            return df
        
        except Exception as e:
            print(f'Failed to create df: {e}')