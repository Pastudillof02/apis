import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Carga las variables de entorno desde el archivo .env

MONGO_URI = os.getenv("MONGO_URI")

mongo = MongoClient(MONGO_URI)
db = mongo.database

geocaches_collection = db.geocaches
logbooks_collection = db.logbooks






