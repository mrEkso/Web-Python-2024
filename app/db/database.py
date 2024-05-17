import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
DB_URL = os.getenv('DB_URL')

client = MongoClient(DB_URL)
db = client[os.getenv('DB_DATABASE')]
