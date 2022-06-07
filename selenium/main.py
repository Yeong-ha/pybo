from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
from multiprocessing import Pool
import pandas as pd
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('--log-level=1')
# driver = webdriver.Chrome(options=options)

key = pd.read_csv('./keyword.txt', encoding='cp949', names=['keyword'])
keyword=[]
[keyword.append(key['keyword'][x]) for x in range(len(key))]

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def image_download(keyword):
    createFolder('./' + keyword + '_high resolution')
    chromedriver = 'C:/Users/AI-00/mysite/selenium/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(3)

    print(keyword, '검색')
    driver.get('https://www.google.co.kr/imghp?hl=ko')

    Keyword = driver.find_element(By.XPATH, '//*[@id="sbtc"]/div/div[2]/input')
    Keyword.send_keys(keyword)

    driver.find_element(By.XPATH, '//*[@id="sbtc"]/button').click()
    print(keyword+' 스크롤중 ..........')
    elem = driver.find_element(By.TAG_NAME, 'body')
    for i in range(10):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    try:
        driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div[1]/div[4]/div[2]/input').click()
        for i in range(10):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except:
        pass

    images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")

    print(keyword+'찾은 이미지 개수:', len(images))

    links = []
    for image in (1, len(images)):
        # try:
        driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').click()
        links.append(driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a').get_attribute('src'))
        driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').click()
        print(keyword + ' 링크 수집 중..... number :' + str(i) + '/' + str(len(images)))
        # except:
        #     continue

    forbidden=0

    for k, i in enumerate(links):
        try:
            url = i
            print(url)
            start = time.time()
            urllib.request.urlretrieve(url, "./" + keyword + "_high resolution" + keyword + "_" + str(k-forbidden) + ".jpg")
            print(str(k+1)+'/'+str(len(links))+' '+keyword+ '다운로드 중.......... Download time: ' + str(time.time() - start)[:5]+ ' 초')
        except:
            forbidden+=1
            continue
    print(keyword+'--다운로드 완료--')

    driver.close()

if __name__=="__main__":
    pool = Pool(processes=1)
    pool.map(image_download, keyword)