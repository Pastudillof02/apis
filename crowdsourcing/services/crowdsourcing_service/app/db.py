import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")

mongo = MongoClient(MONGO_URI)
db = mongo.crowdsourcing_database

colaboradores = db.colaboradores
tareas = db.tareas







