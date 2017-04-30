import random

from helpers import get_stock_index

def make_savings():

    names = [
        "Dangwood National Bank",
        "Sheridan Savings",
        "Seymour Feet Bank & Loan",
        "I.P. Freely Credit Union",
        "Ball State Tower",
        "Musty Buttes Savings"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 0.10

    elif rand < 0.90:

        result["rate"] = rand * 0.55

    else:

        result["rate"] = rand * 0.75

    return result

def make_mutual_fund():

    names = [
        "Edward Jones",
        "Vanguard",
        "Fidelity",
        "Continental",
        "Jim Rivers",
        "Hank Williams",
        "Johnny Cash",
        "Merle Haggard",
        "Karen Farmer",
        "Holly Pidanie",
        "Titus Delly O Jay",
        "Crafty Cats",
        "Seth Lee John",
        "King Arthur"
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
        "Bonnie and Clyde Central Trust",
        "Al Capone National Trust"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 0.75

    elif rand < 0.90:

        result["rate"] = rand

    else:

        result["rate"] = rand * 1.5

    result["risk"] = rand * rand * rand * rand

    return result

def make_bond():

    names = [
        "Kingdom of Asgard",
        "City of Amityville",
        "Transylvania",
        "Neverland",
        "Middle Earth",
        "Alderaan",
        "Snowdonia",
        "North Korea"
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
        "Hank Williams",
        "Garth Brooks",
        "Johnny Cash"
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

def make_horse_racing():

    names = [
        "Horse Racing",
        "Ponzi Scheme",
        "Bingo",
        "Insider Trading",
        "Trip to Vegas",
        "Village Tech Building Bond",
        "Trump Real Estate"
    ]

    result = {
        "name" : random.choice(names)
    }

    rand = random.random()

    if rand < 0.75:

        result["rate"] = rand * 20

    elif rand < 0.90:

        result["rate"] = rand * 50

    else:

        result["rate"] = rand * 100

    result["risk"] = rand * .9

    return result
