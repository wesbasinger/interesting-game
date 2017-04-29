import os

mongo_uri = os.environ["MONGO_URI"]

from pymongo import MongoClient
from bson.objectid import ObjectId

import time

client = MongoClient(mongo_uri)

db = client['interesting']

users = db.users

def initialize_user(user_id):

    user = users.find_one({"user_id" : user_id})

    if not user:

        new_user = {
            "user_id" : user_id,
            "cash" : 10000,
            "accounts" : [],
            "transactions" : [
                {
                    "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
                    "type" : "Initial Deposit",
                    "amount" : 10000,
                    "rate" : "N/A",
                    "duration" : "N/A",
                    "risk" : "N/A"
                }
            ]
        }

        users.insert_one(new_user)

def get_cash(user_id):

    user = users.find_one({"user_id" : user_id})

    if not user:

        return 0

    else:

        return user["cash"]

def get_transactions(user_id):

    user = users.find_one({"user_id" : user_id})

    if not user:

        return []

    else:

        return user["transactions"]
