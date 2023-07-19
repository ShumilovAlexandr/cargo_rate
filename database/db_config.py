import os

from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")

DATABASE_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:' \
               f'{DB_PORT}/{DB_NAME}'
