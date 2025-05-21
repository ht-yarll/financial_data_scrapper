import pytest
from financial_data_scraper.main import main

def test_main_runs_without_error():
    try:
        main()
    except Exception as e:
        assert False, f"main() raised an exception: {e}"
