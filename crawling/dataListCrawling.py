import sys
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm_notebook
from selenium.webdriver.common.action_chains import ActionChains
import time
from collections import OrderedDict

import warnings
warnings.filterwarnings('ignore')

chromedriver_autoinstaller.install()
from selenium.webdriver.chrome.service import Service

s = Service('C:/Users/rlagu/OneDrive/바탕 화면/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s)

# data
driver.get('https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0&tab=position')

# 페이지의 특정 요소가 로드될 때까지 기다림
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.JobCard_container__FqChn'))
)

# 스크롤을 내려서 모든 채용공고가 로드되도록 
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# 채용공고 url 가져오기
urls = 'div.JobCard_container__FqChn > a'
url_raw = driver.find_elements(By.CSS_SELECTOR, urls)

# 채용공고 url 목록 가져오기 (중복 제거, 순서 유지)
url_ordered_dict = OrderedDict()
for url_element in url_raw:
    url = url_element.get_attribute('href')
    if url and url.startswith("https://www.wanted.co.kr/wd/"):  
        url_ordered_dict[url] = None  
url_list = list(url_ordered_dict.keys())

# 채용공고 타이틀 가져오기
titles = 'strong.JobCard_title__ddkwM'
title_raw = driver.find_elements(By.CSS_SELECTOR, titles)

# 채용공고 타이틀 text 변환
title_list = []
for title in title_raw:
    title_text = title.text
    if title_text:  
        title_list.append(title_text)

# 채용공고 회사명 가져오기
companies = 'span.JobCard_companyName__vZMqJ'
company_raw = driver.find_elements(By.CSS_SELECTOR, companies)

# 회사명 text 변환
company_list = []
for company in company_raw:
    company_name = company.text
    if company_name:  
        company_list.append(company_name)

print(len(url_list),len(title_list),len(company_list))

df = pd.DataFrame({'Category': '데이터','URL': url_list, '회사명': company_list, '타이틀': title_list})
print(df.head())

df.to_csv('data_listing.csv', index=False, encoding='utf-8-sig')
