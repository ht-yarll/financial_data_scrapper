from financial_data_scraper.context.etl import extract_transform_load
from financial_data_scraper.pipeline.extractors.usd_currency import USDCurrencyExtract
from financial_data_scraper.pipeline.transformers.bq_pattern_transform import TransformDF
from financial_data_scraper.pipeline.loaders.loading_to_bq import BatchDataOnBQ

from airflow.decorators import task
from airflow.utils.task_group import TaskGroup

class TGUSDCurrency(TaskGroup):
     """
     Extract, Transform and Load tb "usd_currency_history" on bq
     """
     def __init__(self, config, group_id = 'ETL_job_for_usd', tooltip = 'ETL Job', **kwargs):
        super().__init__(group_id = group_id, tooltip = tooltip, **kwargs)

        self.config = config

        @task(task_group = self)
        def usd_currency_etl():
            extract_transform_load(
                self.config,
                extractor = USDCurrencyExtract,
                transformer = TransformDF,
                loader = BatchDataOnBQ,
                table_name= 'usd_currency_history'
            )

        usd_currency_etl()

    