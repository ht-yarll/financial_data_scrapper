from utils.config import load_config
from financial_data_scraper.pipeline.extractors.usd_currencie import USDCurrency
from financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity

def main():
    config = load_config()

    cur = USDCurrency(config)
    cur.extract()

    bloom = BloombergCommodity(config)
    bloom.extract()


if __name__ == "__main__":
    main()
