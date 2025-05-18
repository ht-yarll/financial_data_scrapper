import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By



class SeleniumHelper():
    def __init__(self, config):
        self.url = config['urls']['currencies']
        self.config = config

    def _init_session(self):
        try:
            service = Service()
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            print('✅ Connected')
            return driver
        except Exception as e:
            print('❌ Failed to connect')

    def get_monthly_elements(self, param: str, item_name: str) -> list:
        try:
            driver = self._init_session()
            driver.get(self.url)
            by = getattr(By, param.upper().replace(' ', '_'))

            try:
                dropdowbox = driver.find_element(By.CLASS_NAME, 'historical-data-v2_selection-arrow__3mX7U')
                dropdowbox.click()


                selection = driver.find_elements(By.CLASS_NAME, 'historical-data-v2_menu-row-text__ZgtVH')
                period = 'Mensal'
                for option in selection:
                    if option.text == period:
                        option.click()
                        time.sleep(1.5)
                        print(f'📅 Monthly results')
                        break
                    continue

            except Exception as e:
                print(f'❌ Failed to click on "Mensal": {e}')
                return []
            
            rows = WebDriverWait(driver, 10).until(
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
            print(f'❌ Failed to fetch elements for parameter "{param}": {e}')
            return []

    
    def quit_session(self):
        return self.driver.quit()

    