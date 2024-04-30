import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import datetime
from months import Month
import button

current_date = datetime.date.today()
MSNBC_info = {
    'search query': 'https://www.google.com/search?q={}',
    'search box': '//textarea[@class="gLFyf"]',
    'tools button': '//div[@id="hdtb-tls"]',
    'time select button': '' 
}

def scrape_links(topic, driver, wait, last_updated):
    last_updated_month = last_updated.month
    last_updated_year = last_updated.year
    current_month = current_date.month
    total_links = set()
    search_query = MSNBC_info['search query'].format(topic)
    driver.get(search_query)
    time.sleep(random.randint(2, 4))
    search_box = driver.find_element(By.XPATH, MSNBC_info['search box'])
    search_box.clear()
    search_box.send_keys(topic + ' site: msnbc.com')
    time.sleep(random.randint(2, 4))


