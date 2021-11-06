import warnings
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException 
import base64
from itertools import cycle
import random


chromedriver_path = r'/home/hamza/Desktop/selenium_project/chromedriver_linux64/chromedriver'
warnings.filterwarnings("ignore")
 
# PROXY = "88.157.149.250:8080" # IP:PORT or HOST:PORT

# with open('/home/hamza/Desktop/selenium_project/Grocery_Project_Hamid/luminati_ips-static.txt') as f:
#     proxies = [line.strip() for line in f if line.strip()]
# random.shuffle(proxies)
# proxy_pool = cycle(proxies)
# p = next(proxy_pool)
# proxies = {'https': 'https://' + p, 'http': 'http://' + p}
# print(proxies)

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument('--proxy-server=%s' % proxies)


driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(driver, 10)
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

def check_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output.text
    except NoSuchElementException:
        return " "

def check_exists_by_xpath(driver,xpath):
    try:
        output = driver.find_element_by_xpath(xpath)
        return output.text
    except NoSuchElementException:
        return " "

def check_exists_by_css_click(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output
    except NoSuchElementException:
        return "0"
def check_exists_by_css_selector(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return css_selector
    except NoSuchElementException:
        return "0"


Item_Lookup_Code = []
URL = []
Found = []
Raw_Description = []
Brand = []
complete_data = {}

file = pd.read_csv('/home/hamza/Desktop/selenium_project/Grocery_Project_Hamid/Grocery-CustFacingDescriptions_other.csv',header=0, converters={
                     'Item Lookup Code': str, 'URL': str})

for x in range(len(file['URL'])):  
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)  
    driver.get(file['URL'][x])
    description = check_exists_by_css(driver,'p[class="detailtitle"]>b')
    Raw_Description.append(description)
    Brand.append(check_exists_by_xpath(driver,"//table[@class='detail-list']//tr/td[contains(.,'Brand')]/following-sibling::td"))
    Item_Lookup_Code.append(file['Item Lookup Code'][x])
    if(description != " "):
        Found.append("Yes")
    else:
        Found.append("No")
    
    URL.append(file['URL'][x])
    driver.close()

    complete_data['Item Lookup Code'] = Item_Lookup_Code
    complete_data['URL'] = URL
    complete_data['Found'] = Found
    complete_data['Raw Description'] = Raw_Description
    complete_data['Brand'] = Brand
    
    print(complete_data)
    Data = pd.DataFrame(complete_data)
    Data.to_excel('Final_Output.xlsx' ,index=None)
    Data.to_csv('Final_Output.csv' ,index=None)
    print("Complete Now Thanks You")

    