from datetime import date
from time import sleep

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

   

def extract(url) -> pl.Dataframe:
    res = requests.get(url)
    results = res.json()
    values = results['candles']
    df = pl.DataFrame(values, schema=['timestamp', 'value'], strict=False)
    df = df.with_columns([
        (pl.col('timestamp').cast(pl.Datetime).dt.cast_time_unit('ms')).alias('date')
    ]).select(['date', 'value'])
    print(df.head())
    return df


url =' https://sbcharts.investing.com/charts_xml/cce9bf7363d8e7d1609664b9b9e2d468_max.json'
extract(url = url)