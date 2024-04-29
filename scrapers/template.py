import random
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

'''
urls = ['https://www.cnn.com/2024/04/18/middleeast/us-united-nations-resolution-palestine-membership-intl/index.html',
        'https://www.cnn.com/2024/03/22/middleeast/us-gaza-ceasefire-proposal-veto-intl/index.html?iid=cnn_buildContentRecirc_end_recirc',
        'https://www.cnn.com/2024/04/18/africa/kenya-military-chief-dead-in-helicopter-crash-afr/index.html',
        'https://www.cnn.com/2024/04/15/middleeast/oman-flash-floods-intl-latam/index.html?iid=cnn_buildContentRecirc_end_recirc',
        'https://www.cnn.com/2024/04/17/americas/toronto-airport-heist-arrests/index.html',
        'https://www.cnn.com/2024/04/11/europe/russia-navalny-memoir-intl/index.html',
        'https://www.cnn.com/2013/11/04/us/violence-against-u-s-politicians-and-diplomats-fast-facts/index.html',
        'https://www.cnn.com/2023/10/24/politics/supreme-court-florida-anti-drag-law/index.html',
        'https://www.cnn.com/2024/04/18/politics/biden-kennedy-family-endorsements-rfk-jr/index.html'
        ]

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('div', class_='headline headline--has-lowertext')
    if header:
        print(f'Found header for: {url}')

    main_body = soup.find('div', class_='article__content')
    if main_body:
        print(f'Found main body for: {url}')
'''

def get_links(soup):
    class_string = 'card.container__item.container__item--type-media-image.container__item--type-.container_list-images-with-description__item.container_list-images-with-description__item--type-'
    links = set()
    articles = soup.select(f'div.{class_string}')
    for article in articles:
        a_tag = article.find('a')
        if a_tag and a_tag['href']:
            links.add(a_tag['href'])
    return links

AI_search_query = 'https://www.cnn.com/search?q=artificial+intelligence&size=20&sort=newest&types=article'
palestine_search_query = 'https://www.cnn.com/search?q=palestine&size=20&sort=newest&types=article'
# setting up selenium web driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)

# passing in the url query
driver.get(palestine_search_query)
# waiting for results to load
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# searching for the amount of links we need to get
search_count_element = soup.select(f'div.search__results-count')[0].text
countEndIndex = search_count_element.index(' for')
count = int(search_count_element[31:countEndIndex])

# getting the button we need to navigate search results
pagination_button = driver.find_element(By.CLASS_NAME, 'pagination-arrow-right')

total_links = set()
while count - 1 > len(total_links):
    # adding all the links per each search result page
    total_links.update(get_links(soup))
    try:
        pagination_button.click()
        # need this random wait so don't get rate limited
        time.sleep(random.randint(5, 10))
        # waiting for the next page to load (better to wait for a specific element that indicates the page has loaded)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search__results')))  
        next_page = driver.page_source
        soup = BeautifulSoup(next_page, 'html.parser')
        # have to get the button again
        pagination_button = driver.find_element(By.CLASS_NAME, 'pagination-arrow-right')

    except Exception as e:
        print("Reached the last page or encountered an error:", e)
        break

print(total_links)
print(len(total_links))
print(count)
driver.quit()










