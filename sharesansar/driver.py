from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date, datetime
from scrape_table_all import scrape_table
from return_dates import return_dates

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.sharesansar.com/today-share-price")

wait = WebDriverWait(browser, 10)
select2_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection--single')))
select2_dropdown.click()

# enter sector type here
sectorType = "Commercial Bank"

option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{sectorType}")]')))
option.click()

def set_date_input(date_input_id, day_str):
    day = datetime.strptime(day_str, '%Y-%m-%d')
    date_box = wait.until(EC.element_to_be_clickable((By.ID, date_input_id)))
    date_box.clear()
    date_box.send_keys(day.strftime('%Y-%m-%d'))

# start and end date here (YYYY,MM,DD)
sdate = date(2020, 1, 1)
edate = date(2024, 5, 28)
dates = return_dates(sdate, edate)

for day in dates:
    set_date_input('fromdate', day)
    
    search_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_todayshareprice_submit')))
    search_button.click()

    time.sleep(8)

    html = browser.page_source
    scrape_table(data=html, date=day)

browser.close()
