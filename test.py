#-*- coding:utf-8 -*-
from selenium import webdriver
from mariadb import MariaDB
import logging , datetime
import logging.handlers
from time import sleep
import numpy as np
import re

log = logging.getLogger('log_custom')
log.setLevel(logging.DEBUG)
log.propagate = True
formatter = logging.Formatter("%(asctime)s;[%(levelname)s];%(message)s",
                              "%Y-%m-%d %H:%M:%S")
## 그냥 처리
#fileHandler = logging.FileHandler('./log.txt' ,mode = "w")
streamHandler = logging.StreamHandler()
log_max_size = 10 * 512
log_file_count = 5
## 용량별 처리
### log.txt에는 용량만큼 쌓고
### backupCount 수만큼 쌓는 것을 저장함.
# fileHandler = logging.handlers.RotatingFileHandler(filename='./log.txt',
#                                                    maxBytes=log_max_size,
#                                                    backupCount=log_file_count,
#                                                    mode = "w",
#                                                   )
## 시간별 처리
### log.txt에는 when 시간 동안 쌓이고
### backupCount에서 그 형식의 이름으로 저장
fileHandler = logging.handlers.TimedRotatingFileHandler(
    filename='/home/ec2-user/hangyeol/sweden-news/news_api_client/logs/news_api/news_api.log',
    when = "M" ,  # W0
    backupCount= 4 ,
    atTime=datetime.time(0, 0, 0)
)
fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.DEBUG)

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
log.addHandler(fileHandler)
log.addHandler(streamHandler)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='/home/ec2-user/hangyeol/sweden-news/news_api_client/chromedriver',chrome_options=chrome_options)

driver.implicitly_wait(3)

driver.get('https://live.aftonbladet.se/supernytt')

db = MariaDB()
def wordsSorting(sentence):
    if not sentence is None:
        sentence = sentence.strip()
        sentence = re.sub('\d', '', sentence)
        sentence = re.sub('[–-–=().#/?:$},"\']','',sentence)
        words = sentence.split()
        for word in words:
            db.addCountOfWords(word.lower())
def insertNewsInfo(title,domain,author,published_dt,content):
    published_dt = re.sub('[TZ]',' ',published_dt)
    db.insertNewsInfo(title,domain,author,published_dt,content)
    wordsSorting(content)
    wordsSorting(title)
#find_element_by_name('HTML_name')
#find_element_by_id('HTML_id')
#find_element_by_xpath('/html/body/some/xpath')
#find_element_by_css_selector('#css > div.selector')
#find_element_by_class_name('some_class_name')
#find_element_by_tag_name('a')
driver.find_elements_by_tag_name('article')
#driver.find_element_by_class_name('news-list__item').click()
from bs4 import BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
textGroup = soup.select('article > p,h2[itemprop="headline"],time[itemprop="datePublished"],span')
content = ''
title = ''
previousTitle = ''
author = ''
published_dt = ''
order = 0

for n in textGroup:
    if n.name == 'time':
        if order == 1:
            print('this is content')
            insertNewsInfo(title,'Aftonbladet',author,published_dt,content)
            content=''
            order = 0
        published_dt = n["datetime"]
    if n.name == 'span':
        author = n.text
    if n.name == 'h2':
        title = n.text
        order = 1
        cnt = db.checkIfTitleExists(title)
        if cnt == 0:
            log.info('checkIfTitleExists() \'{}\' exists'.format(title))
            order = 100
            break
    if n.name == 'p':
        content += n.text
        content += ' '
if order != 100:
    insertNewsInfo(title,'Aftonbladet',author,published_dt,content)
driver.quit()