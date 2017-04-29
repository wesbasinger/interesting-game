import os
import uuid

mongo_uri = os.environ["MONGO_URI"]

from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import datetime

from helpers import *

client = MongoClient(mongo_uri)

db = client['interesting']

users = db.users

def get_user(user_id):

    user = users.find_one({"user_id" : user_id})

    if not user:

        return None

    else:

        return user

def initialize_user(user_id):

    user = get_user(user_id)

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
                    "rate" : "NA",
                    "duration" : "NA",
                    "risk" : "NA"
                }
            ]
        }

        users.insert_one(new_user)

def get_cash(user_id):

    user = get_user(user_id)

    if not user:

        return 0

    else:

        return user["cash"]

def get_transactions(user_id):

    user = get_user(user_id)

    if not user:

        return []

    else:

        return user["transactions"]

def create_savings(user_id, bank, rate, amount):

    if amount > get_cash(user_id):

        return {"error" : True, "message" : "insufficient funds"}

    else:

        account = {

            "type" : "savings",
            "account_id" : str(uuid.uuid1()),
            "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "bank" : bank,
            "rate" : float(rate),
            "amount" : float(amount)

        }

        transaction = {
            "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "type" : "Saving Deposit",
            "amount" : amount,
            "duration" : "NA",
            "rate" : rate,
            "risk" : 0
        }

        return  db.users.update(

            {"user_id" : user_id},
            {
                "$push" : {
                    "accounts" : account, "transactions" : transaction
                },
                "$inc" : {
                    "cash" : -1 * amount
                }
            }
        )

def get_accounts(user_id):

    user = get_user(user_id)

    accounts = user["accounts"]

    for account in accounts:

        hours = elapsed_hours(account["deposit_time"])

        if account["type"] == "savings":

            # set additional needed value for display in account manager
            account["current_value"] = calculate_compound_interest(account["amount"], account["rate"], hours)
            account["maturation_value"] = account["current_value"]
            account["duration"] = "NA"
            account["mature"] = True
            account["risk"] = 0

    return accounts
