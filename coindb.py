import pymysql
import os
import pandas as pd

class coinDB():
    def __init__(self, host='52.79.239.69', exchange='upbit'):
        self.db = pymysql.connect(host=host,
                                  port=3306,
                                  user='root',
                                  password=os.environ['MYSQL_PASSWORD'],
                                  db=exchange,
                                  charset='utf8',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
            
        self.cursor = self.db.cursor()
        
    def execute(self, query):
        try:
            self.cursor.execute(query)
            if ('SELECT' in query) or ('SHOW' in query):
                return pd.DataFrame(self.cursor.fetchall())
            else:
                return pd.DataFrame()
        except pymysql.err.ProgrammingError as e:
            print(e)

    def rollback(self):
        self.db.rollback()
    
    def close(self):
        self.db.close()

if __name__ == '__main__':
    host = '52.79.239.69'
    upbitDB = coinDB(host)
    query = "SHOW DATABASES;"
    result = upbitDB.execute(query)
    print(result)
    upbitDB.execute("USE upbit;")
    query = "SELECT DATABASE();"
    result = upbitDB.execute(query)
    print(result)
    upbitDB.close()