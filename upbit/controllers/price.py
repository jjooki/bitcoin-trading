import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import UpbitConfig
from ..models.mysql.price import RealtimePrice
from ..modules.my_upbit import Myupbit

config = UpbitConfig()
connection_string = config.mysql_connection_string('bitcoin')
engine = create_engine(connection_string, echo=False)

def get_realtime_price():
    # 호가정보조회
    upbit = Myupbit()

if __name__ == '__main__':
    BASE = declarative_base()
    BASE.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    user = Test('james', 30, 180)
    session.add(user)
    session.commit()
    
    obj = session.query(Test).filter(Test.name == 'james').first()
    