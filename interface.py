import os
import uuid

mongo_uri = os.environ["MONGO_URI"]

from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import datetime

from helpers import *

INSUFFICIENT_FUNDS = {
    "error" : True, "message" :
    "You do not have sufficient funds."
}

client = MongoClient(mongo_uri)

db = client['interesting']

users = db.users

def get_user(user_id):

    user = users.find_one({"user_id" : user_id})

    if not user:

        return None

    else:

        return user

def initialize_user(user_id, name, picture):

    user = get_user(user_id)

    if not user:

        new_user = {
            "user_id" : user_id,
            "name" : name,
            "picture" : picture,
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

        return INSUFFICIENT_FUNDS

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

def create_money_market(user_id, bank, rate, amount, risk):

    if amount > get_cash(user_id):

        return INSUFFICIENT_FUNDS

    else:

        account = {

            "type" : "money market",
            "account_id" : str(uuid.uuid1()),
            "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "bank" : bank,
            "rate" : float(rate),
            "amount" : float(amount),
            "risk" : float(risk)
        }

        transaction = {
            "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "type" : "Money Market Deposit",
            "amount" : amount,
            "duration" : "NA",
            "rate" : rate,
            "risk" : float(risk)
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

def create_bond(user_id, name, rate, risk, amount, duration):

    if amount > get_cash(user_id):

        return INSUFFICIENT_FUNDS

    else:

        account = {

            "type" : "government bond",
            "account_id" : str(uuid.uuid1()),
            "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "bank" : name,
            "rate" : rate,
            "amount" : amount,
            "risk" : risk,
            "duration" : duration
        }

        transaction = {
            "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "type" : "Government Bond Purchase",
            "amount" : amount,
            "duration" : duration,
            "rate" : rate,
            "risk" : risk
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

def create_compound_deposit(user_id, name, rate, amount, duration):

    if amount > get_cash(user_id):

        return INSUFFICIENT_FUNDS

    else:

        account = {

            "type" : "compound deposit",
            "account_id" : str(uuid.uuid1()),
            "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "bank" : name,
            "rate" : rate,
            "amount" : amount,
            "duration" : duration,
            "risk" : 0
        }

        transaction = {
            "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
            "type" : "Compound Deposit",
            "amount" : amount,
            "duration" : duration,
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

        elif account["type"] == "mutual fund":

            account["current_value"] = account["amount"] * get_stock_index()
            account["maturation_value"] = account["current_value"]
            account["duration"] = "NA"
            account["mature"] = True
            account["risk"] = 0

        elif account["type"] == "money market":

            account["current_value"] = calculate_compound_interest(account["amount"], account["rate"], hours)
            account["maturation_value"] = account["current_value"]
            account["duration"] = "NA"
            account["mature"] = True

        elif account["type"] == "government bond" or account["type"] == "compound deposit":

            account["maturation_value"] = calculate_compound_interest(account["amount"], account["rate"], account["duration"])

            if hours >= account["duration"]:

                account["mature"] = True
                account["current_value"] = account["maturation_value"]

            else:

                account["mature"] = False
                account["current_value"] = "NA"

        elif account["type"] == "horse racing":

            account["current_value"] = calculate_compound_interest(account["amount"], account["rate"], hours)
            account["maturation_value"] = account["current_value"]
            account["duration"] = "NA"
            account["mature"] = True

    return accounts


def create_horse_racing(user_id, name, rate, risk, amount):

    if amount > get_cash(user_id):

        return INSUFFICIENT_FUNDS

    account = {

        "type" : "horse racing",
        "account_id" : str(uuid.uuid1()),
        "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
        "bank" : name,
        "rate" : rate,
        "amount" : amount,
        "duration" : "NA",
        "risk" : risk
    }

    transaction = {
        "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
        "type" : "Horse Racing",
        "amount" : amount,
        "duration" : "NA",
        "rate" : rate,
        "risk" : risk
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



def delete_account(user_id, account_id):

    users.update(
        {"user_id" : user_id},
        {
            "$pull" : {
                "accounts" : {"account_id" : account_id}
            }
        }
    )

def add_cash(user_id, cash_amount):

    transaction = {
        "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
        "type" : "Withdrawal",
        "amount" : cash_amount,
        "duration" : "NA",
        "rate" : "NA",
        "risk" : 0
    }

    users.update(
        {"user_id" : user_id},
        {
            "$inc" : {
                "cash" : float(cash_amount)
            },
            "$push" : {
                "transactions" : transaction
            }
        }
    )

def create_mutual_fund(user_id, name, price, shares):

    if price * shares > get_cash(user_id):

        return INSUFFICIENT_FUNDS

    account = {

        "type" : "mutual fund",
        "account_id" : str(uuid.uuid1()),
        "deposit_time" : time.strftime('%Y-%m-%d %H:%M:%S'),
        "bank" : name,
        "rate" : "NA",
        "amount" : shares

    }

    transaction = {
        "timestamp" : time.strftime('%Y-%m-%d %H:%M:%S'),
        "type" : "Mutual Fund Purchase",
        "amount" : price * shares,
        "duration" : "NA",
        "rate" : price,
        "risk" : 0
    }

    return  db.users.update(

        {"user_id" : user_id},
        {
            "$push" : {
                "accounts" : account, "transactions" : transaction
            },
            "$inc" : {
                "cash" : -1 * price * shares
            }
        }
    )

def get_aggregate_accounts():

    results = users.aggregate(
        [
            {"$unwind" : "$accounts"},
            {
                "$project" :
                    {
                        "_id" : 0,
                        "cash" : 1,
                        "name" : 1,
                        "picture" : 1,
                        "user_id" : 1,
                        "amount" : "$accounts.amount",
                        "rate" : "$accounts.rate",
                        "deposit_time" : "$accounts.deposit_time",
                        "risk" : "$accounts.risk",
                        "duration" : "$accounts.duration"
                    }
                },
                {
                    "$match" : {
                        "$or" :[
                        {"risk": {"$lt": 0.70}},
                        {"risk": {"$exists": "false"}}]
                            }
                }
        ]
    )

def make_valuations():

    _users = users.find()

    results = []

    for user in _users:

        result =  {
            "name" : user["name"],
            "picture" : user["picture"],
            "value" : user["cash"]
        }

        for account in user["accounts"]:

            hours = elapsed_hours(account["deposit_time"])

            if account["type"] == "money market" and account["risk"] < 0.70:

                result["value"] += calculate_compound_interest(account["amount"], account["rate"], hours)

            elif account["type"] == "mutual fund":

                result["value"] += account["amount"] * get_stock_index()

            elif account["type"] == "compound deposit" and is_mature(account["deposit_time"], account["duration"]):

                result["value"] += calculate_compound_interest(account["amount"], account["rate"], account["duration"])

            elif account["type"] == "government bond" and is_mature(account["deposit_time"], account["duration"]) and account["risk"] < 0.70:

                result["value"] += calculate_compound_interest(account["amount"], account["rate"], account["duration"])

            elif account["type"] == "savings":

                result["value"] += calculate_compound_interest(account["amount"], account["rate"], hours)

            elif account["type"] == "horse racing" and account["risk"] < 0.50:

                result["value"] += calculate_compound_interest(account["amount"], account["rate"], hours)

        results.append(result)

    newlist = sorted(results, key=lambda k: k['value'], reverse=True)

    return newlist
