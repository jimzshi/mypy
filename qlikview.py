from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import time

#initialize web browser;
option = webdriver.ChromeOptions()
option.add_argument(r'--user-data-dir=e:\home\jimzs\AppData\Local\Google\Chrome\User Data\webdriver')
driver = webdriver.Chrome(chrome_options=option)

driver.implicitly_wait(30)
driver.maximize_window()

#start test
try:
    driver.get("http://localhost/qlikview/index.htm")

    driver.find_element_by_link_text('PSN_Test.qvw').click()
    time.sleep(3)

    driver.find_element_by_xpath('//*[@id="4"]/div[3]/div/div[1]/div[7]').click()
    time.sleep(3)

    driver.find_element_by_link_text('Close').click()
    time.sleep(3)

finally:
    driver.quit()
