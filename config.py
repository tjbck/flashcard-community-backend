from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

from secrets import token_bytes
from base64 import b64encode
import os

load_dotenv(find_dotenv())

####################################
# ENV (dev,test,prod)
####################################

ENV = os.environ.get("ENV", "dev")

####################################
# DB
####################################

MONGODB_URL = os.environ.get(
    "MONGODB_URL", "mongodb://root:root@localhost:27017/?authSource=admin"
)

DB_CLIENT = MongoClient(f"{MONGODB_URL}")
DB = DB_CLIENT["flashcard-community"]

####################################
# SESSION_SECRET_KEY
####################################

SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "t0p-s3cr3t")
