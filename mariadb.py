import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

class MariaDB():
    def __init__(self):
        self.config = {
            'user': 'hangyeol',
            'password': 'hangyeol',
            'host': 'localhost',
            'database': 'king_of_data'
        }    
    def checkIfTitleExists(self, title):
        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cur = cnx.cursor()
            cur.execute('select count(*) as cnt from title where title =\'{}\';'.format(title))
            row = cur.fetchone()
            cnt = int(row[0])
            if cnt == 0:
                cur = cnx.cursor()
                cur.execute('insert into title (title) values (\'{}\')'.format(title))
                cnx.commit()
                return 1
            else:
                return 0
        finally:
            if cur:
                cur.close()
            if cnx:
                cnx.close()
    def insertNewsInfo(self, category,title,domain,author,description,published_dt,content):
        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cur = cnx.cursor()
            temp = 'insert into swedish_news_info (category,title,domain,author,description,published_dt,content) values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'.format(category,title,domain,author,description,published_dt,content)
            print(temp)
            cur.execute('insert into swedish_news_info (category,title,domain,author,description,published_dt,content) values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'.format(category,title,domain,author,description,published_dt,content))
            cnx.commit()
        finally:
            if cur:
                cur.close()
            if cnx:
                cnx.close()
    def addCountOfWords(self,word):
        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            today = datetime.today().strftime('%Y-%m-%d')
            cur = cnx.cursor()
            cur.execute('select count(*) as cnt from swedish_words where word = \'{}\' and id = \'{}\''.format(word, today))
            #for row in cur.fetchall():
            #    print(row)
            row = cur.fetchone()
            cnt = int(row[0])
            if cnt == 0:
                print(word)
                cur.execute('insert into swedish_words (word, count, id) values (\'{}\',1, \'{}\')'.format(word, today))
                cnx.commit()
            else:
                print(word)
                cur.execute('update swedish_words set count = count+1 where word = \'{}\' and id = \'{}\''.format(word, today))
                cnx.commit()
        finally:
            if cur:
                cur.close()
            if cnx:
                cnx.close()
        

