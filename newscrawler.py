#-*- coding:utf-8 -*-
from selenium import webdriver
from mariadb import MariaDB
import numpy as np
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='/home/ec2-user/hangyeol/sweden-news/news_api_client/chromedriver',chrome_options=chrome_options)

driver.implicitly_wait(3)

driver.get('https://live.aftonbladet.se/supernytt')

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
notices = soup.select('article > p,h2[itemprop="headline"]')

db = MariaDB()
for n in notices:
    if n.name == 'h2':
        cnt = db.checkIfTitleExists(unicode(n.text).encode('utf8'))
        if cnt == 0:
            print('end')
            break
    else:    
        text = n.text.strip()
        text = re.sub('\d', '', text)
        text = re.sub('[–-–=().#/?:$},\"]','',text)
        words = text.split()
        words_arr = np.append(words_arr,words)
for word in words_arr:
    db.addCountOfWords(unicode(word.lower()).encode('utf8'))
driver.quit()

words_arr = np.array([])
text = n.text.strip()
text = re.sub('\d', '', text)
text = re.sub('[–-–=().#/?:$},\"]','',text)
words = text.split()
words_arr = np.append(words_arr,words)