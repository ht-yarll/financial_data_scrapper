import unicodedata
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, InvalidOperation
from app.interfaces.transformer_strat_interface import TransformStrategy
import polars as pl
import pandas as pd


class TransformDF(TransformStrategy):
    def __init__(self):
        ...
    
    def transform(self, df: pl.DataFrame) -> pd.DataFrame:
        try:
            decimal_cols = ['last', 'open', 'high', 'low', 'value']
            df_values_parsed = df.with_columns(
                pl.col(col)
                .map_elements(self._parse_decimal, return_dtype = pl.Float64)
                for col in decimal_cols if col in df.columns
            )

            df_variation_parsed = df_values_parsed.with_columns(
                pl.col('variation')
                .map_elements(self._parse_variation, return_dtype = pl.Float64)
                if 'variation' in df_values_parsed.columns else df_values_parsed
            )

            df_sanitizing_columns = df_variation_parsed.with_columns(
                pl.col(column)
                .map_elements(self._sanitize, return_dtype=str) 
                for column in df_variation_parsed.columns
                if df_variation_parsed.schema[column] == pl.Utf8
            )
            
            df_final = df_sanitizing_columns.to_pandas()
            print(f'✅ Df ready to load')
            
            return df_final
        
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
    
    def _parse_decimal(self, value):
        if not isinstance(value, str):
            return value
        
        value = re.sub(r'[^\d,.\-]', '', value)
        if value.count(',') == 1 and value.count('.') == 0:
            value = value.replace(',', '.')
        value = re.sub(r'(?<=\d)[,.](?=\d{3}\b)', '', value)
        try:
            return float(value)
        except (ValueError, InvalidOperation):
            return None
        
    def _parse_variation(self, value):
        if not isinstance(value, str):
            return value
        
        value = value.strip().replace('%', '')
        try:
            return float(value)
        except ValueError:
            return None