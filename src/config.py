import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.dbenv'))


DB_DRIVER = os.environ.get('DB_DRIVER')
DB_CONNECTOR = os.environ.get('DB_CONNECTOR')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
