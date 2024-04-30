import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

current_date = datetime.date.today()

CNN_info = {
    'article container': 'card.container__item.container__item--type-media-image.container__item--type-.container_list-images-with-description__item.container_list-images-with-description__item--type-',
    'search query': 'https://www.cnn.com/search?q={}&size=20&sort=newest&types=article',
    'search count element': 'div.search__results-count',
    'pagination button': 'pagination-arrow-right',
    'search results element': 'search__results'
}

def scrape_link(topic, driver, wait, last_updated):
    search_query = CNN_info['search query']
    topic = topic.replace(' ', '+')
    search_query = search_query.format(topic)
    driver.get(search_query)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    search_count_element = soup.select(f"{CNN_info['search count element']}")[0].text
    countEndIndex = search_count_element.index(' for')
    count = int(search_count_element[31:countEndIndex])
    pagination_button = driver.find_element(By.CLASS_NAME, CNN_info['pagination button'])
    total_links = set()

    while count - 1 > len(total_links):
        total_links.update(get_links(soup))
        try:
            pagination_button.click()
            # need this random wait so don't get rate limited
            time.sleep(random.randint(5, 10))
            # waiting for the next page to load (better to wait for a specific element that indicates the page has loaded)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, CNN_info['search results element'])))  
            next_page = driver.page_source
            soup = BeautifulSoup(next_page, 'html.parser')
            # have to get the button again
            pagination_button = driver.find_element(By.CLASS_NAME, CNN_info['pagination button'])

        except Exception as e:
            print("Reached the last page or encountered an error:", e)
            break
    
    print(total_links)
    print(len(total_links))

def get_links(soup):
    class_string = CNN_info['article container']
    links = set()
    articles = soup.select(f'div.{class_string}')
    for article in articles:
        a_tag = article.find('a')
        if a_tag and a_tag['href']:
            links.add(a_tag['href'])
    return links


        


        



