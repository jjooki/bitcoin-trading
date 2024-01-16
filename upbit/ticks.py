import pandas as pd
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from coindb import coinDB
import time

# reference : https://inmoonlight.github.io/2021/02/04/Pandas-Dataframe-iterations/#

class Ticks:
    def __init__(self, ticker:str, count:int):
        self.tick = pd.DataFrame()
        self.ticker = ticker
        self.table_name = self.ticker.replace('-', '_') + '_Ticks' #naming rule
        if count > 500:
            self.count = 500
        else:
            self.count = count

    def ticks(self) -> pd.DataFrame:
        url = "https://api.upbit.com/v1/trades/ticks?"
        url += "market={}&count={}".format(self.ticker, self.count)

        headers = {"accept": "application/json"}
        res = requests.get(url, headers=headers)
        json_data = json.loads(res.text)
        self.present = pd.DataFrame(json_data)
    
    def concat(self):
        df = self.present
        last = self.tick['sequential_id'].iloc[0]
        if self.tick.empty:
            self.tick = df
        else:
            df = df[df['sequential_id'] > last]
            self.tick = pd.concat([df, self.tick], axis=0)

    def get_tick(self):
        return self.tick

    def get_tablename(self):
        return self.table_name

    def create_table(self):
        db = coinDB()
        sql = f'CREATE TABLE {self.table_name}'
        sql += """{
            market Varchar(10) NOT NULL
            , trade_date_utc Char(12) NOT NULL
            , trade_time_utc Char(8) NOT NULL
            , timestamp BIGINT NOT NULL
            , trade_price DOUBLE NOT NULL
            , trade_volume DOUBLE NOT NULL
            , prev_closing_price DOUBLE NOT NULL
            , change_price DOUBLE NOT NULL
            , ask_bid Char(3) NOT NULL
            , sequential_id BIGINT PRIMARY KEY
        }"""
        try:
            db.execute(sql)
            db.close()
        except:
            print("Already this db table exists!")

    def insert(self):
        db = coinDB()
        # check which table is selected and move
        if db.execute("SELECT DATABASE();").iloc[0,0] != 'upbit':
            db.execute(f"USE upbit;")
        for row in self.tick.itertuples():
            value = str(list(row.to_dict().values))[1:-1]
            query = f"INSERT INTO {self.table_name} VALUES ({value});\n"
            db.execute(query)
        db.close()

    def insert(self):
        pass