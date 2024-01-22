import numpy as np
import pandas as pd
import re
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")




def fetchFullReviews(reviewurl):
    driver = webdriver.Chrome()
    url = reviewurl
    delay = 10 # delay time 30sec
    button_exists = True

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)

    review_counts = []
    for links in soup.find_all(text=re.compile(r"^[0-9,]* Reviews$")):
        review_count = links.get_text().strip()    #Text is stripped
        review_counts.append(review_count)                 #Added to list
        revnumber = int(int((str(review_counts[0]).replace(' Reviews','')).replace(',',''))/25)

    print(review_counts[0])
    print(revnumber)

    while button_exists == True: # repeat this process while load more button exists
        try:
            load_more_button = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ipl-load-more__button"]'))) # find the Load More button by xpath
            load_more_button.click() # click on Load More Button
        except:
            button_exists = False # if we get exception, it means that the button is no longer existing and we loaded all reviews
                #time.sleep(3)
                #driver.find_element(By.ID, css_selector).click()
            #except:
               # pass
    
    return driver.page_source

'''   for i in tqdm(range(revnumber)):
        try:
            css_selector = 'load-more-trigger'
            element_present = EC.presence_of_element_located((By.ID, css_selector))
            WebDriverWait(driver, delay).until(element_present)
            button_exists = True # True value means that load more button exists
'''
    

   
