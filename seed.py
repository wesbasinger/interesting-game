import random

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
