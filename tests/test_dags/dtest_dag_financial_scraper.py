import pytest
from airflow.models import DagBag

def test_dag_loaded():
    dagbag = DagBag
    dag = dagbag.get_dag('financial_data_scraper')
    assert dag is not None
    assert dag.dag_id == 'financial_data_scraper'
    task_ids = [t.task_id for t in dag.tasks]
    # Ajuste os nomes conforme suas tasks reais
    assert any('usd_currency' in tid for tid in task_ids)
    assert any('chinese_pmi' in tid for tid in task_ids)
    assert any('bloomberg' in tid or 'bloom_comm' in tid for tid in task_ids)