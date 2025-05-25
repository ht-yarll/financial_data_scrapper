from datetime import timedelta
import pendulum


from airflow.decorators import dag
from airflow.models import Variable
from airflow.providers.http.operators.http import HttpOperator


default_args = {
    "owner": "Humphry Torres(ht-yarll)",
    "start_date": pendulum.datetime(2025, 1, 1, tz="America/Sao_Paulo"),
    "retries":3,
    'retry_delay': timedelta(minutes=2)
}


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
    endpoint='/'
    )

    return invoke_scraper_cloud_run

# Execution -------------------------------------------------------------------------

financial_data_scraper()