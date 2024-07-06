from decouple import config
from pymongo import MongoClient

MONGO_URL = config('MONGO_URL')

client = MongoClient(MONGO_URL)

db = client.projects




