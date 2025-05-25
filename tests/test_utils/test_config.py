import pytest

from api.utils.config import load_config

def test_if_config_is_reading():
    config = load_config()

    assert isinstance(config, dict)