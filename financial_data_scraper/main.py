from utils.config import load_config
from financial_data_scraper.pipeline.extractors.usd_currencie import USDCurrency
from financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity
from financial_data_scraper.pipeline.extractors.chinese_cash_services import ChineseCashServices

def main():
    config = load_config()

    cur = USDCurrency(config)
    cur.extract()

    bloom = BloombergCommodity(config)
    bloom.extract()

    chin_pmi = ChineseCashServices(config)
    chin_pmi.extract()


if __name__ == "__main__":
    main()
