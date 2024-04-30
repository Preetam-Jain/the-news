from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import scrape_cnn
import scrape_fox
import scrape_msnbc
from datetime import datetime

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)
topics = ['artificial intelligence', 'palestine', 'climate change', 'presidential election', 'tiktok']
last_updated = datetime(2024, 1, 1) # Year, Month, Day
#scrape_cnn.scrape_links(topics[0], driver, wait, last_updated)
#scrape_fox.scrape_links(topics[0], driver, wait, last_updated)
scrape_msnbc.scrape_links(topics[0], driver, wait, last_updated)
driver.quit()
