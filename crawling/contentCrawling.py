import pandas as pd
import numpy as np
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm


chromedriver_autoinstaller.install()


driver = webdriver.Chrome()

# URL 데이터 로드
url_load = pd.read_csv('combined_list.csv', encoding='utf-8-sig')
num_list = len(url_load)
print(f"Total URLs: {num_list}")

target_dict = {}  

# 수집할 글 갯수 정하기
number = num_list

for i in tqdm(range(number)):
    url = url_load['URL'][i]
    driver.get(url)
    time.sleep(5)  # 페이지 로딩 대기

    try:
        target_info = {}

        position = driver.find_element(By.CSS_SELECTOR, '.JobHeader_className__HttDA h2').text
        name = driver.find_element(By.CSS_SELECTOR, '.JobHeader_className__HttDA > div > h6').text
        description = driver.find_element(By.CSS_SELECTOR, '.JobDescription_JobDescription__VWfcb>p:nth-child(3) > span').text
        requirement = driver.find_element(By.CSS_SELECTOR, '.JobDescription_JobDescription__VWfcb>p:nth-child(5) > span').text
        preferred = driver.find_element(By.CSS_SELECTOR, '.JobDescription_JobDescription__VWfcb>p:nth-child(7) > span').text
              
        like_element = driver.find_element(By.CSS_SELECTOR, 'div.Reactions_Reactions__root__3cKAu > button > span.Button_Button__label__1Kk0v').text
        like = int(like_element.split()[-1])  

        target_info['position'] = position
        target_info['company_name'] = name
        target_info['description'] = description
        target_info['requirement'] = requirement
        target_info['preferred'] = preferred
        target_info['like'] = like

        target_dict[i] = target_info
        time.sleep(1)
       

    except Exception as e:
        print(f"Error at {i}: {e}")
        continue
    
    # 중간 저장: 100개의 URL을 처리할 때마다 파일로 저장
    if (i + 1) % 100 == 0 or i == num_list - 1:
        interim_df = pd.DataFrame.from_dict(target_dict, 'index')
        interim_df.to_csv(f'content_{i+1}.csv', index=False, encoding='utf-8-sig')
        print(f"저장 완료: content_{i+1}.csv")
   

driver.quit()

#result_df = pd.DataFrame.from_dict(target_dict, 'index')
#result_df.to_csv('content.csv', index=False, encoding='utf-8-sig')

