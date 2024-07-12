from decouple import config
from pymongo import MongoClient

MONGO_URL = config('MONGO_URL_LOCAL') # Lembrar de mudar para MONGO_URL quando for para produção

client = MongoClient(MONGO_URL)

db = client.projects




