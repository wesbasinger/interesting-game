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

def make_money_market():

    names = [
        "Jesse James Bank",
        "Pancho Villa Loan Institution",
        "Corleone Credit Union",
        "Goodfellas",
        "Bonnie and Clyde Central Trust"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 1.5

    elif rand < 0.90:

        result["rate"] = rand * 2

    else:

        result["rate"] = rand * 2.5

    result["risk"] = rand * rand * rand * rand

    return result

def make_bond():

    names = [
        "Kingdom of Asgaurd",
        "City of Amityville",
        "Transvania",
        "Neverland",
        "Middle Earth"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 1.5

    elif rand < 0.90:

        result["rate"] = rand * 2

    else:

        result["rate"] = rand * 2.5

    result["risk"] = rand * rand * rand * rand

    result["duration"] = random.choice([5, 10, 15, 20, 50, 100])

    result["amount"] = random.choice([100, 500, 1000, 2000, 5000, 10000])

    return result

def make_compound_deposit():

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

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand

    elif rand < 0.90:

        result["rate"] = rand * 1.25

    else:

        result["rate"] = rand * 1.5

    result["duration"] = random.choice([5, 10, 15, 20, 50, 100])

    result["amount"] = random.choice([100, 500, 1000, 2000, 5000, 10000])

    return result
