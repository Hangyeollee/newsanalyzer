#-*- coding:utf-8 -*-
from newsapi import NewsApiClient
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

#get newsapi
newsapi = NewsApiClient(api_key='6539a1fd189b4a2b9f68671e4f521514')
db = MariaDB()
def wordsSorting(sentence):
    if not sentence is None:
        sentence = sentence.strip()
        sentence = re.sub('\d', '', sentence)
        sentence = re.sub('[–-–=().#/?:$},\"\']','',sentence)
        words = sentence.split()
        for word in words:
            db.addCountOfWords(word)
def newsInfoSorting(source):
    for n in source:
        title = n['title']
        if title != '':
            cnt = db.checkIfTitleExists(title)
            if cnt == 0:
                log.info('checkIfTitleExists() \'{}\' exists'.format(title))
                continue
        wordsSorting(title)
        domain = n['source']['name']
        author = n['author']
        description = n['description']
        wordsSorting(description)
        if (not description is None) and ('\'' in description or '\"' in description):
            description = description.replace('\"','\\\"').replace('\'','\\\'')
        published_dt = n['publishedAt'].replace('T',' ',1).replace('Z','',1)
        content = n['content']
        wordsSorting(content)
        if (not content is None) and ('\'' in content or '\"' in content):
            content = content.replace('\"','\\\"').replace('\'','\\\'')
        db.insertNewsInfo('business',title,domain,author,description,published_dt,content)

top_headlines_business = newsapi.get_top_headlines(category='business', country='se')
top_headlines_entertainment = newsapi.get_top_headlines(category='entertainment', country='se')
top_headlines_health = newsapi.get_top_headlines(category='health', country='se')
top_headlines_science = newsapi.get_top_headlines(category='science', country='se')
top_headlines_sports = newsapi.get_top_headlines(category='sports', country='se')
top_headlines_technology = newsapi.get_top_headlines(category='technology', country='se')
newsInfoSorting(top_headlines_business['articles'])
newsInfoSorting(top_headlines_entertainment['articles'])
newsInfoSorting(top_headlines_health['articles'])
newsInfoSorting(top_headlines_science['articles'])
newsInfoSorting(top_headlines_sports['articles'])
newsInfoSorting(top_headlines_technology['articles'])
