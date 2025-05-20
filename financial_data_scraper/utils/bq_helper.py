import os

from financial_data_scraper.utils.config import load_config

from dotenv import load_dotenv
import pandas as pd
import pandas_gbq as pdgbq
from google.cloud import bigquery

class BigQueryHelper:
    def __init__(self):
        self.config = load_config()
        load_dotenv(self.config['env'])
    
        self.bq = bigquery.Client()
        self.project_id = self.config['project_id']
        
    def make_query(self, query: str):
        try:
            query_job = self.bq.query(query)
            result = query_job.result()
            print('👍 Query job successful')
            return result
        
        except Exception as e:
            print (f'👎 Query not made:\n{e}')
            return None


    def load_pd_dataframe_on_bq(self, df: pd.DataFrame, table_name: str):
        try:
            table_id = f"{self.config['services']['bigquery']['dataset']}.{table_name}"
            pdgbq.to_gbq(df, destination_table=table_id, if_exists='replace')

        except Exception as e:
            print(f'😞 Unable to load DataFrame on BQ: {e}')
