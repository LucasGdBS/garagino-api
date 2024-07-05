from decouple import config
from pymongo import MongoClient
import gridfs

MONGO_URL = config('MONGO_URL')

client = MongoClient(MONGO_URL)

db = client.projects

collection_name = db["garagino_projects_collection"]

fs = gridfs.GridFS(db)


