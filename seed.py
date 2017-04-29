import random

from helpers import get_stock_index

def make_savings():

    names = [
        "Dangwood National Bank",
        "Sheridan Savings",
        "Seymour Feet Bank & Loan",
        "IP Freely Credit Union",
        "Ball State Tower"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 0.30

    elif rand < 0.90:

        result["rate"] = rand * 0.75

    else:

        result["rate"] = rand

    return result

def make_mutual_fund():

    names = [
        "Edward Jones",
        "Vanguard",
        "Fidelity",
        "Continental",
        "Jim Rivers",
        "Hank Williams"
    ]

    result = {
        "name" : random.choice(names)
    }

    result["price"] = get_stock_index()

    return result
