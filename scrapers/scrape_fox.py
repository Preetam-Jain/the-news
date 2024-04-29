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

current_date = datetime.date.today()

FOX_info = {
    'search count element': 'num-found',
    'search query': 'https://www.foxnews.com/search',
    'search box': '//div[@class="search-form"]/input',
    'search submit': '//div[@class="search-form"]//a',
    'load more': '//div[@class="button load-more"]/a',
    'content type button': '//div[@class="filter content"]/button',
    'select articles button': '//div[@class="filter content"]//input[@title="Article"]',
    'min month': '//div[@class="date min"]//div[@class="sub month"]/button',
    'min month selector': '//div[@class="date min"]//div[@class="sub month"]//li[@id="{}"]',
    'min day': '//div[@class="date min"]//div[@class="sub day"]/button',
    'min day selector': '//div[@class="date min"]//div[@class="sub day"]//li[@id="{}"]',
    'min year': '//div[@class="date min"]//div[@class="sub year"]/button',
    'min year selector': '//div[@class="date min"]//div[@class="sub year"]//li[@id="{}"]',
    'max month': '//div[@class="date max"]//div[@class="sub month"]/button',
    'max month selector': '//div[@class="date max"]//div[@class="sub month"]//li[@id="{}"]',
    'max day': '//div[@class="date max"]//div[@class="sub day"]/button',
    'max day selector': '//div[@class="date max"]//div[@class="sub day"]//li[@id="{}"]',
    'max year': '//div[@class="date max"]//div[@class="sub year"]/button',
    'max year selector': '//div[@class="date max"]//div[@class="sub year"]//li[@id="{}"]'
}

def scrape(topic, driver, wait, last_updated):
    last_updated_month = last_updated.month
    last_updated_year = last_updated.year
    current_month = current_date.month

    for month in range(last_updated_month, current_month + 1):
        range_of_days = format_range(month)
        for i in range(len(range_of_days)):
            first_day, last_day = range_of_days[i]
            driver.get(FOX_info['search query'])
            time.sleep(random.randint(2, 4))
            content_type_button = get_button(wait, FOX_info['content type button'])
            click(content_type_button)
            select_articles_button = get_button(wait, FOX_info['select articles button'])
            click(select_articles_button)
            select_range(month, (first_day, last_day), last_updated_year, wait)
            search_box = driver.find_element(By.XPATH, FOX_info['search box'])
            search_box.send_keys(topic)
            time.sleep(random.randint(1, 2))
            submit_button = get_button(wait, FOX_info['search submit'])
            click(submit_button)
            load_more_button = get_button(wait, FOX_info['load more'])
            while load_more_button is not None:
                click(load_more_button)
                load_more_button = get_button(wait, FOX_info['load more'])

# each month has a different range of days we need to sort for, we have to do 10 days at a time or we get too many articles
# the max amount of articles the search can pull is 100 so we have to get less than that per search
def format_range(month_number):
    if month_number in (Month.JANUARY.value, Month.MARCH.value, Month.MAY.value, Month.JULY.value, 
                        Month.AUGUST.value, Month.OCTOBER.value, Month.DECEMBER.value):
        return [(1, 10), (11, 20), (21, 31)]
    elif month_number in (Month.APRIL.value, Month.JUNE.value, Month.SEPTEMBER.value, Month.NOVEMBER.value):
        return [(1, 10), (11, 20), (21, 30)]
    elif month_number is Month.FEBRUARY.value:
        if current_date.year % 4 == 0:
            return [(1, 10), (11, 20), (21, 29)]
        else:
            return [(1, 10), (11, 20), (21, 28)]
        
def format_with_leading_zero(number):
    return f"{number:02d}"  # formats the number with a leading zero if it's a single digit

def click_date_component(button_name, value, selector_format, wait):
    # click the button to open the dropdown
    button = get_button(wait, FOX_info[button_name])
    click(button)
    
    # select the value from the dropdown
    value_string = format_with_leading_zero(value)
    selector_xpath = selector_format.format(value_string)
    selection_button = get_button(wait, selector_xpath)
    click(selection_button)

# selecting the time range we want articles from
def select_range(month, day_range, year, wait):
    # select min date
    click_date_component('min month', month, FOX_info['min month selector'], wait)
    click_date_component('min day', day_range[0], FOX_info['min day selector'], wait)
    click_date_component('min year', year, FOX_info['min year selector'], wait)

    # select max date
    click_date_component('max month', month, FOX_info['max month selector'], wait)
    click_date_component('max day', day_range[1], FOX_info['max day selector'], wait)
    click_date_component('max year', year, FOX_info['max year selector'], wait)

        
def get_button(wait, xpath):
    try:
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        return None


# clicking button passed in and waiting a random time between 2 and 4 seconds
def click(button):
    button.click()
    time.sleep(random.randint(2, 4))

