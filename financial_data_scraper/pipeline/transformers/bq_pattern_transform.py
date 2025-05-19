import unicodedata
import re
from financial_data_scraper.interfaces.transformer_strat_interface import TransformStrategy
import polars as pl
import pandas as pd


class PatternBQ(TransformStrategy):
    def __init__(self):
        ...
    
    def transform(self, df: pl.DataFrame) -> pd.DataFrame:
        try:
            df = self.df.map_rows(self._sanitize)
            df_ready_to_load = df.to_pandas()
            print(f'✅ Df ready to load')
            return df_ready_to_load
        
        except Exception as e:
            print(f'❌ Failed to transform df: {e}')

    def _sanitize(self, text):
        if not isinstance(text, str):
            return text
        
        if re.match(r'^-?\d+[.,]?\d*$', text):
            return text

        text = unicodedata.normalize("NFKD", text)  
        text = text.encode("ASCII", "ignore").decode("ASCII")  
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)  
        text = re.sub(r'[^A-Za-z0-9\s]', '', text)  
        text = re.sub(r'\s+', ' ', text).strip()

        return text