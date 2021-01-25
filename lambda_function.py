#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup

regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
pattern_email = re.compile(fr"{regex_email}")

class SetHaveIBeenPwned:
    url = "https://haveibeenpwned.com/unifiedsearch/"

def lambda_handler(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    driver.set_page_load_timeout(30)
    
    email = event["email"]
    url = SetHaveIBeenPwned.url + email
    driver.get(url)
    driver.implicitly_wait(10)
    html_data = driver.page_source
    current_url = driver.current_url
    
    html_len = len(html_data)
    soup_data = BeautifulSoup(html_data, 'html.parser')
    data = soup_data.find("pre")
    driver.close()
    driver.quit()
    
    if 200 < html_len:
        try:

            data_dict = json.loads(data.text)
            return {"ok": True, "response": data_dict, "url": current_url, "email": email}
        except NoSuchElementException as err:
            return {"ok": False, "response": repr(err)}
        except AttributeError as err:
            if "AttributeError: 'NoneType' object has no attribute 'text'" in repr(err):
                return {"ok": False, "response": repr(err)}

    else:
        return {"ok": False, "response": "Data Not Found"}


