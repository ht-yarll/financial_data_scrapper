from api.interfaces.loader_strat_interface import LoadStrategy
from api.utils.bq_helper import BigQueryHelper

from dotenv import load_dotenv
import pandas as pd

class BatchDataOnBQ(LoadStrategy, BigQueryHelper):
    def __init__(self, config):
        self.config = config
        self.env = load_dotenv(config['env'])

    def load(self, df:pd.DataFrame, table_name:str):
        self.load_pd_dataframe_on_bq(df, table_name)