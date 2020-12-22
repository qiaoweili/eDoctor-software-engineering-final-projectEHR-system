"""
header.py:: connect to mongoDB
"""

import pymongo
from config.config import MONGO_URL

conn = pymongo.MongoClient(MONGO_URL)
db = conn['edoctor']
