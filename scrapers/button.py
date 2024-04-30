from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import random

def get_button(wait, xpath):
    try:
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        return None


# clicking button passed in and waiting a random time between 2 and 4 seconds
def click(button):
    button.click()
    time.sleep(random.randint(2, 4))