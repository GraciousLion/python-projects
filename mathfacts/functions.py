def forceInt():
    res = input()
    while True:
        try:
            return int(res)
        except ValueError:
            res = input('Please enter an integer:\n')


def weighFact(fact):
    # factname = tuple(fact.keys())[0]
    weight = sum(fact['recentTimes']) * 0.07 + sum(fact['recentlyWrong'])
    return weight / len(fact['recentTimes']) if weight > 0 else 0.2


def practicing(condition, problems=None, time=None, limit=None):
    if condition == 'forever':
        return True
    if condition == 'problems':
        if problems < limit:
            return True
        else:
            return False
    if condition == 'minutes':
        if time <= limit:
            return True
        else:
            return False
    return False


def saveToFile(facts):
    with open('mathfacts/facts.py', 'w') as history:
        history.write('facts = ')
        history.write(str(facts))
