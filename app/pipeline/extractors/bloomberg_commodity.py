from app.utils.selenium_helper import SeleniumHelper
from app.interfaces.extractor_strat_interface import ExtractStrategy

import polars as pl

class BloombergCommodityExtract(ExtractStrategy):
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
            schema = {'date':pl.Utf8, 'value':pl.Utf8, 'variation':pl.Utf8}   
            df = pl.DataFrame(values, schema = schema)
            print(f'🐻‍❄️ Dataframe Bloomberg_Commodity generated with schema {schema}')
            selenium.quit_session()
            
            return df
        
        except Exception as e:
            print(f'Failed to create df Bloomberg: {e}')