from datetime import timedelta
import pendulum

from financial_data_scraper.utils.config import load_config
from financial_data_scraper.taskgroups.tg_bloomberg_commodity import TGBloombergCommodity
from financial_data_scraper.taskgroups.tg_usd_currency import TGUSDCurrency
from financial_data_scraper.taskgroups.tg_chinese_pmi import TGCHinesePMI

from airflow.decorators import dag
from airflow.models import Variable
from airflow.providers.http.operators.http import HttpOperator


default_args = {
    "owner": "Humphry Torres(ht-yarll)",
    "start_date": pendulum.datetime(2025, 1, 1, tz="America/Sao_Paulo"),
    "retries":3,
    'retry_delay': timedelta(minutes=2)
}
config = load_config()

@dag(
    "financial_data_scraper",
    default_args=default_args,
    #schedule_interval='0 22 * * 1-5',
    catchup=False,
    tags=["MARKET"],
)


def financial_data_scraper():
    """
    DAG to fetch financial data from invest.com
    """

    invoke_scraper_cloud_run = HttpOperator(
    task_id='invoke_function',
    http_conn_id="scraper_cloud_run_extraction",
    method='GET',
    endpoint='/scraper'
)
    usd_value = TGUSDCurrency(config)
    chinese_pmi = TGCHinesePMI(config)
    bloom_comm = TGBloombergCommodity(config) 

    return invoke_scraper_cloud_run >> [usd_value, chinese_pmi, bloom_comm]


# Execution -------------------------------------------------------------------------

financial_data_scraper()