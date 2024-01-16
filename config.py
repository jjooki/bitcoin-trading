import os

from dotenv import load_dotenv

load_dotenv()

class UpbitConfig:
    access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
    secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
    server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')
    QUOTATION_REQUEST_LIMIT_PER_SECOND = 30
    EXCHANGE_REQUEST_LIMIT_PER_SECOND = 8
    RDB_HOST = os.getenv('RDB_HOST')
    RDB_PORT = os.getenv('RDB_PORT')
    RDB_USER = os.getenv('RDB_USER')
    RDB_PASSWORD = os.getenv('RDB_PASSWORD')
    
    def mysql_connection_string(self, database: str):
        return 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'\
            .format(user=self.RDB_USER,
                    password=self.RDB_PASSWORD,
                    host=self.RDB_HOST,
                    port=self.RDB_PORT,
                    database=database)