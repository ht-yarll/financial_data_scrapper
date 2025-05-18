from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class SeleniumHelper():
    def __init__(self, url):
        self.url = url

    def _init_session(self):
        try:
            service = Service()
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            print('✅ Connected')
            return driver
        except Exception as e:
            print('⭕ Failed to connect')

    def get_monthly_elements(self) -> list:
        try:
            driver = self._init_session()
            driver.get(self.url)

            dropdowbox = driver.find_element(By.CLASS_NAME, 'historical-data-v2_selection-arrow__3mX7U')
            dropdowbox.click()

            selection = driver.find_elements(By.CLASS_NAME, 'historical-data-v2_menu-row-text__ZgtVH')
            period = 'Mensal'
            i = 0
            while i < len(selection):
                print(selection[i].text)
                if (selection[i].text) == period:
                    selection[i].click
                    print(f'📅 Period Selected! {period}')
                    break
                i += 1
                    

        except Exception as e:
            print(f'Failed to click: {e}')
            return []
        #<span class="historical-data-v2_menu-row-text__ZgtVH">Mensal</span>

s = SeleniumHelper('https://br.investing.com/currencies/usd-cny-historical-data')

s.get_monthly_elements()