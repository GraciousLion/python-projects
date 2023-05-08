#!/usr/bin/env python3
"""
This is a math facts "game". It has a bunch of math facts, grouped by type, in an external pickle file. It asks you them, and it records whether you were right and how long you took. And when you press CTRL-C, it writes your results to another pickle file so you can pick up where you left off last time.

The next thing I'm going to add is multiple users
"""
import facts, random, time, sys
from functions import *

# This is how far back you want the engine to remember your time and accuracy history.
maxHist = 5

try:
    condition, limit = (
        ('forever', None)
        if len(sys.argv) < 3
        else (sys.argv[1], float(sys.argv[2]))
    )
except ValueError:
    condition, limit = 'forever', None

times = []
accuracy = []
factlist = tuple(facts.facts.keys())
factWeights = list(map(lambda name: weighFact(facts.facts[name]), factlist))
# print(factlist, '\n', factWeights)

try:
    beganAt = time.time()
    while practicing(
        condition,
        problems=len(times),
        time=(time.time() - beganAt) / 60,
        limit=limit,
    ):
        # *******************
        fact = random.choices(factlist, factWeights, k=1)[0]
        if fact[2] == 'x':
            continue
        firstNum = round(random.random()) if fact[2] in '+x' else 0
        print(
            f'\n\x1b[1m{fact[firstNum]} {fact[2]} {fact[not firstNum]} = ',
            end='',
        )
        beginQ = time.time()
        res = forceInt()
        endQ = time.time()

        # *******************
        facts.facts[fact]['recentTimes'].append(endQ - beginQ)
        facts.facts[fact]['recentlyWrong'].append(res != fact[3])
        while len(facts.facts[fact]['recentTimes']) > maxHist:
            facts.facts[fact]['recentTimes'].pop(0)
        while len(facts.facts[fact]['recentlyWrong']) > maxHist:
            facts.facts[fact]['recentlyWrong'].pop(0)
        factWeights[factlist.index(fact)] = weighFact(facts.facts[fact])

        # *******************
        times.append(endQ - beginQ)
        accuracy.append(res == fact[3])

        # *******************
        if res == fact[3]:
            print('\x1b[0mCorrect!')
        else:
            print(
                f'\x1b[33mIncorrect. The correct answer is \x1b[0;34m{fact[3]}\x1b[0m.'
            )
        time.sleep(1)
    raise KeyboardInterrupt('Limit exceeded.')

except KeyboardInterrupt:
    print(
        f'\nYou did math facts for \x1b[35;1m{round((time.time()-beganAt)/60)}\x1b[0m minute{"" if round((time.time()-beganAt)/60) == 1 else "s"}.\n'
    )
    print(
        f'You averaged \x1b[35;1m{round(sum(times)/len(times), 1)}\x1b[0m seconds per fact. \nYou got \x1b[1;35m{sum(accuracy)} out of {len(accuracy)}\x1b[0m facts right. \nYou answered \x1b[35;1m{sum(accuracy)/len(accuracy):.1%}\x1b[0m of questions correctly.'
    )
    print('Storing your results...')
    saveToFile(facts.facts)
    print('Done!')
