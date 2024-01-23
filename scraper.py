from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


def fetchFullReviews(url):
    driver = webdriver.Chrome()
    delay = 10 # delay time 30sec
    button_exists = True

    driver.get(url)

    while button_exists == True: # repeat this process while load more button exists
        try:
            load_more_button = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ipl-load-more__button"]'))) # find the Load More button by xpath
            load_more_button.click() # click on Load More Button
        except:
            button_exists = False # if we get exception, it means that the button is no longer existing and we loaded all reviews
            
    elements=WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review-container")))
    print(len(elements))

    revcontainers = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
    
    return revcontainers


    


    

   
