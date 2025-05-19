import unicodedata
import re
from datetime import datetime
from financial_data_scraper.interfaces.transformer_strat_interface import TransformStrategy
import polars as pl
import pandas as pd


class PatternBQ(TransformStrategy):
    def __init__(self):
        ...
    
    def transform(self, df: pl.DataFrame) -> pd.DataFrame:
        try:
            df_sanitizing_columns = df.with_columns([
                pl.col(col)
                .map_elements(self._sanitize, return_dtype=str) 
                for col in df.columns
            ])

            dates_aliases = ['date', 'data', 'datetime']
            df_date_parsed = df_sanitizing_columns.with_columns(
                pl.col(col)
                .map_elements(self._parse_date, return_dtype = str)
                for col in df.columns if col in dates_aliases 
            )
            df_final = df_date_parsed.to_pandas()
            df_ready_to_load = df_final.infer_objects()
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
    
    def _parse_date(self, date):
        if not isinstance(date, str):
            return date
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            try:
                dt = datetime.strptime(date, "%d/%m/%Y")
            except ValueError:
                return date
        return dt.strftime("%y-%m-%d")