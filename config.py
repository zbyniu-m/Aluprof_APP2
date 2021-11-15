import os
from dotenv import load_dotenv
from pathlib import Path
import cx_Oracle
import pyodbc

# load env constans
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)

# connections string for data:
cx_Oracle.init_oracle_client(lib_dir=r"C:\\instatntclient\\instantclient_19_12")
cx_connection = cx_Oracle.connect(user=os.environ.get('CX_LOGIN'), password=os.environ.get('CX_PASSWORD'),
                                  dsn=os.environ.get('CX_DNS'), encoding="UTF-8")

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=MEDION\ZBYNIO;"
                      "Database=SCADA;"
                      "Trusted_Connection=yes;")

connections = [{
        'id': 0,
        'name': 'oracle',
        'connection': cx_connection
},
    {
        'id': 1,
        'name': 'mssql',
        'connection': cnxn
    }
]
# Scheduler
schedule_time = '07:10'

# Config classes
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
    JWT_EXPIRED_MINUTES = 30
    WTF_CSRF_SECRET_KEY = os.environ.get('SECRET_KEY')
    CX_USER = os.environ.get('CX_LOGIN')
    CX_PW = os.environ.get('CX_PASSWORD')
    CX_DNS = os.environ.get('CX_DNS')
    DEF_DIR = r'C:\Users\USER\Desktop\Aluprof_APP'



class DevelopmentConfig(Config):
    DB_FILE_PATH = base_dir / 'aluprof_app' / 'database.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    DEBUG = True
    TESTING = True


class ProductingConfig(Config):
    DB_FILE_PATH = base_dir / 'database_production.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductingConfig
}
