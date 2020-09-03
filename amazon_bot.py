from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
import time

class AmazonBot(object):
    def __init__(self, items):
        self.amazon_url = "https://www.amazon.com/"
        self.items = items

        self.profile = webdriver.FirefoxProfile()
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_profile=self.profile, firefox_options=self.options)
        
        self.driver.get(self.amazon_url)

        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.html = self.soup.prettify("utf-8")


    def search_items(self):
        urls = []
        prices = []
        names = []

        for item in self.items:
            print(f"Searching for {item}...")

            self.driver.get(self.amazon_url)
            select = Select(self.driver.find_element_by_id("searchDropdownDesscription"))
            select.select_by_visible_text("All Departments")

            search_input = self.driver.find_element_by_id("twotabsearchtextbox")
            search_input.send_keys(item)

            time.sleep(2)
            
            wait = WebDriverWait(self.driver, self.explicit_wait)
            wait.until(EC.presence_of_all_elements_located((By.ID, "twotabsearchtextbox")))

            search_button = self.driver.find_element_by_xpath("//*[@id='nav-search']/form/div[2]/div/input")
            search_button.click()

            time.sleep(2)

            t = self.driver.find_element_by_id("result_0")
            asin = t.get_attribute("data-asin")
            url = "https://www.amazon.com/dp/" + asin
            price = self.get_product_price(url)
            name = self.get_product_name(url)

            prices.append(price)
            urls.append(url)
            names.append(name)

            print(name)
            print(price)
            print(url)


    def get_product_price(self):
        pass

    def get_product_name(self):
        pass

    def close_session(self):
        pass

