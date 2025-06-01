from datetime import datetime, date, timedelta
from time import sleep

from app.utils.config import load_config

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import requests
import polars as pl


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

    def click_on_period(self):
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
        

    def select_date(self):
        driver = self._init_session()
        driver.get(self.url)

        try:
            calendar_dropdown = driver.find_element(By.XPATH, "//div[contains(@class, 'flex flex-1 flex-col')]")
            sleep(5)
            calendar_dropdown.click()
            print(f'Click! 🐁')

            calendar_show = calendar_dropdown.find_elements(By.XPATH, f"//input[(@type='date' and @max!='{date.today()}')]")
            # calendar_show.clear()
            # calendar_show.send_keys('2020-07-01')
            # print(f'Date Changed 🐁')
            
        except Exception as e:
            print(f'Failed to click: {e}')
            return None

# s = SeleniumHelper('https://br.investing.com/currencies/usd-cny-historical-data')

# s.select_date()

   

def extract(url) -> pl.DataFrame:
    res = requests.get(url)
    results = res.json()
    df = pl.DataFrame(results, strict=False)
    return df

def select_date_interval_five_years(self):
        try:
            date_drop = self.driver.find_element(By.CSS_SELECTOR, 'div.flex.flex-1.flex-col.justify-center')
            date_drop.click()

            end_date = datetime.today()
            start_date = end_date - timedelta(days=5*365)

            end_date_str = end_date.strftime("%m/%d/%Y")
            start_date_str = start_date.strftime("%m/%d/%Y")

            start_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[name="startDate"]'))
            )

            end_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="endDate"]'))
            )

            self.driver.execute_script("arguments[0].removeAttribute('readonly')", start_input)
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", end_input)

            print("Preenchendo datas...")
            start_input.clear()
            start_input.send_keys(start_date_str)
            end_input.clear()
            end_input.send_keys(end_date_str)

            print("Buscando botão aplicar...")
            apply_button = self.driver.find_element(By.CSS_SELECTOR,'div.flex.cursor-pointer.items-center.gap-3.rounded.bg-v2-blue')
            apply_button.click()
            print('📅 Date interval set to five years')

        except Exception as e:
            print(f'❌ Failed t select date interval: {e}')

def see_coonection_with_api(url, config):
    headers = config['services']['requests']['headers']
    res = requests.post(url, headers=headers)

    if res.status_code != 200:
        print('Failed to connect')
        raise ValueError("API reaised an error", res.status_code)

    print('Success')


# Exec --------------------------------------
config = load_config()
url = 'https://data.investing.com/api/s/track'

see_coonection_with_api(url, config)