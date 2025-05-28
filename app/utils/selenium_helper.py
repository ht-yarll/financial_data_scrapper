import os
import time
from datetime import datetime, timedelta
from typing import List, Tuple

from app.utils.selenium_remote_connection_v2 import RemoteConnectionV2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By



class SeleniumHelper(RemoteConnectionV2):
    def __init__(self, url):
        self.url = url # site to scrape
        self.driver = self._init_session()

    def get_monthly_elements(self) -> List[Tuple[str, str, str]]:
        try:
            self.driver.get(self.url)

            self._click_on_period('Mensal')
            time.sleep(1.5)

            rows = self.driver.find_elements(By.XPATH, '//table[contains(@class, "historicalTbl")]/tbody/tr')

            elements_list = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                try:
                    record = {
                        "date": cells[0].text,
                        "last": cells[1].text,
                        "open": cells[2].text,
                        "high": cells[3].text, 
                        "low": cells[4].text,
                        "variation": cells[6].text
                    }
                    elements_list.append(record)

                except Exception as e:
                    continue
            
            return elements_list

        except Exception as e:
            print(f'❌ Failed to fetch elements for parameter: {e}')
            return []

    
    def _init_session(self):
        try:
            selenium_con = RemoteConnectionV2(self.get_selenium_url(), keep_alive = True)
            selenium_con.set_remote_connection_authentication_headers()
            chrome_options = Options()
            driver = webdriver.Remote(selenium_con, DesiredCapabilities.CHROME, options = chrome_options)
            print('✅ Connected')
            return driver
            
        except Exception as e:
            print(f'❌ Failed to connect: {e}')

    def quit_session(self):
        return self.driver.quit()
        
    def _click_on_period(self, period: str):
        try:
            selection = self.driver.find_elements(By.CLASS_NAME, 'historical-data-v2_menu-row-text__ZgtVH')
            period = 'Mensal' # Mensal -> Monthly | Diário -> Daily | Semanal -> Weekly
            for option in selection:
                if option.text == period:
                    option.click()
                    time.sleep(1.5)
                    print(f'📅 Monthly results fetched')
                    break
                continue

        except Exception as e:
            print(f'❌ Failed to click on "Mensal": {e}')
            return []
        
    
