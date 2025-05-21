import pytest

from dags.financial_data_scraper.utils.config import load_config

def test_if_config_is_reading():
    config = load_config()

    assert isinstance(config, dict)