from datetime import timedelta
import pendulum

from financial_data_scraper.taskgroups.tg_bloomberg_commodity import TGBloombergCommodity
from financial_data_scraper.taskgroups.tg_usd_currency import TGUSDCurrency
from financial_data_scraper.taskgroups.tg_chinese_pmi import TGBloombergCommodity

from airflow.decorators import dag
from airflow.models import Variable

default_args = {
    "owner": "Humphry Torres(ht-yarll)",
    "start_date": pendulum.datetime(2025, 1, 1, tz="America/Sao_Paulo"),
    "retries":3,
    'retry_delay': timedelta(minutes=2)
}
config = ''

@dag(
    "financial_data_scraper",
    default_args=default_args,
    schedule_interval='0 22 * * 1-5',
    params = config,
    catchup=False,
    tags=["MARKET"],
)

def financial_data_scraper(config):
    """
    DAG to fetch
    """
    ...


# Execution -------------------------------------------------------------------------
