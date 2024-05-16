import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)
db = client['financial_exchange']
