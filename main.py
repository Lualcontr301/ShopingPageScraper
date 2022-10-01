import time
from unicodedata import name

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

URL = 'https://tiendamia.com/primaveradeofertas/'
PRODUCT = 'miband 6'
SIDE_FILTERS = ['Relojes', 'Montevideo']


class MeLiScraper:

    def click_on_filters(self, filters):
        for filter in filters:
            self.driver.find_element_by_xpath(f'//a[@aria-label="{filter}"]').click()

    @staticmethod
    def convert_to_float(text):
        return float(text.replace('.', '').replace(',', '.'))

    def run(self):
        
        self.driver = webdriver.Chrome(executable_path='/opt/ShopingPageScraper/chromedriver')
        self.driver.get(URL)
        input_search = self.driver.find_element_by_xpath('//input[@name="amz"]')
        input_search.send_keys(PRODUCT)
        input_search.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//li[contains(text(), "$25 to $50")]'))
            ).click()
        except TimeoutException as e:
            print('Element not found in 2 secconds')
            raise e
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,'//h3[contains(text(), "Featured Brands")]/../..//ul/li'))
            )
            for element in elements:
                if "Xiaomi" in element.text:
                    element.click()
        except TimeoutException as e:
            print('Element not found in 2 secconds')
            raise e
        
        items_list = self.driver.find_elements_by_xpath('//div[contains(@class, "tabs-content-container js-result-amz")]//div[contains(@class, "body-result ")]/div[contains(@class, "item button-border")]/a')
        names_dict = {}
        count = 0
        for item in items_list:
            try:
                names_dict[f'Product {count}'] = {
                    'Name': item.find_element_by_xpath('./div[contains(@class, "item-name")]').text,
                    'Price': item.find_element_by_xpath('./div[contains(@class, "item-price")]/div[contains(@class, "item-real-price")]/div/span[contains(@class,"dollar_price")]').text
                }
                count += 1
            except StaleElementReferenceException as SE:
                print("Error stale")
                pass
        print(f"Names: {names_dict}")
        # print(f"Total Elements: {len(names)}")
        
        """
        return [{
            'name': item.find_element_by_xpath('//div[contains(@class, "item-name")]').text,
             #'price': item.find_element_by_xpath('//div[contains(@class, "item-real-price")]/div/span[contains(@class, "dollar_price")]').text,
        } for item in items_list]
        """
        input("Continue")


if __name__ == '__main__':
    result = MeLiScraper().run()
    print(result)