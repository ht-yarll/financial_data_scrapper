import os
import time
from typing import List, Tuple

from api.utils.selenium_remote_connection_v2 import RemoteConnectionV2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By



class SeleniumHelper(RemoteConnectionV2):
    def __init__(self, url):
        self.url = url
        self.driver = self._init_session()

    def get_monthly_elements(self) -> List[Tuple[str, str, str]]:
        try:
            self.driver.get(self.url)

            self._click_on_period('Mensal')

            rows = WebDriverWait(self.driver, 10).until(
                ec.presence_of_all_elements_located((By.XPATH, '//table//tbody/tr'))
            )

            elements_list = []
            for row in rows:
                try:
                    date = row.find_element(By.XPATH, './td[1]/time')
                    value = row.find_element(By.XPATH, './/td[contains(@class, "font-normal") and contains(text(), ",")]')
                    variation = row.find_element(By.XPATH,'.//td[contains(@class, "font-bold") and contains(text(), "%")]')
                    pack = (date.text, value.text, variation.text)
                    elements_list.append(pack)
                except Exception as e:
                    continue
 
            return elements_list

        except Exception as e:
            print(f'❌ Failed to fetch elements for parameter: {e}')
            return []


    def quit_session(self):
        return self.driver.quit()
    
    
    def _init_session(self):
        try:
            selenium_con = RemoteConnectionV2(self.selenium_url, keep_alive = True)
            selenium_con.set_remote_connection_authentication_headers()
            driver = webdriver.Remote(selenium_con, DesiredCapabilities.CHROME)
            print('✅ Connected')
            return driver
        
        except Exception as e:
            print('❌ Failed to connect')

        
    def _click_on_period(self, period: str):
        try:
            dropdowbox = self.driver.find_element(By.CLASS_NAME, 'historical-data-v2_selection-arrow__3mX7U')
            dropdowbox.click()

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
        
    def _select_date_interval(self):
        ...
    