from utils.config import load_config
from financial_data_scraper.pipeline.extractors.usd_currencie import USDCurrency
from financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity
from financial_data_scraper.pipeline.extractors.chinese_cash_services import ChineseCashServices
from financial_data_scraper.pipeline.transformers.bq_pattern_transform import PatternBQ
from financial_data_scraper.pipeline.loaders.loading_to_bq import BatchDataOnBQ

def main():
    config = load_config()
    treat = PatternBQ()
    load = BatchDataOnBQ()

    cur = USDCurrency(config)
    cur_treated = treat.transform(cur.extract())

    bloom = BloombergCommodity(config)
    bloom_treated = treat.transform(bloom.extract())

    chin_pmi = ChineseCashServices(config)
    pmi_to_be_treated = treat.transform(chin_pmi.extract())


if __name__ == "__main__":
    main()
