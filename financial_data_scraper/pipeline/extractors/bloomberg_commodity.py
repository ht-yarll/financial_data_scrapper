from csv import DictWriter, QUOTE_ALL

from financial_data_scraper.utils.selenium_helper import SeleniumHelper
from financial_data_scraper.interfaces.extractor_strat_interface import ExtractStrategy

class BloombergCommodity(ExtractStrategy):
    def __init__(self, config):
        self.config = config
    
    def extract(self):
        with open('data/bloomberg.csv', 'w', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, ['date', 'value', 'variation'], quoting=QUOTE_ALL)
            writer.writeheader()

            selenium = SeleniumHelper(self.config['urls']['commodity'])
            elements = selenium.get_monthly_elements()
            i = 1
            for e in elements:
                bloomberg_dict = {
                    "date": e[0],
                    "value": e[1],
                    "variation": e[2]
                }
                writer.writerow(bloomberg_dict)
                print(f'Written row {i}')
                i += 1