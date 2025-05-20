from financial_data_scraper.utils.config import load_config
from financial_data_scraper.pipeline.extractors.usd_currency import USDCurrency
from financial_data_scraper.pipeline.extractors.bloomberg_commodity import BloombergCommodity
from financial_data_scraper.pipeline.extractors.chinese_cash_services import ChineseCashServices
from financial_data_scraper.pipeline.transformers.bq_pattern_transform import TransformDF
from financial_data_scraper.pipeline.loaders.loading_to_bq import BatchDataOnBQ

def main():
    config = load_config()
    treat = TransformDF()
    load = BatchDataOnBQ(config)

    cur = USDCurrency(config)
    cur_treated = treat.transform(cur.extract())
    load.load_pd_dataframe_on_bq(cur_treated, 'usd_currencie_history')

    bloom = BloombergCommodity(config)
    bloom_treated = treat.transform(bloom.extract())
    load.load_pd_dataframe_on_bq(bloom_treated, 'bloomberg_commodity_history')

    chin_pmi = ChineseCashServices(config)
    pmi_treated = treat.transform(chin_pmi.extract())
    load.load_pd_dataframe_on_bq(pmi_treated, 'chinese_pmi_caixin_services')


if __name__ == "__main__":
    main()
