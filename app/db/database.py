import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)
db = client['financial_exchange']
