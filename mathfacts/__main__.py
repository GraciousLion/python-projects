#!/usr/bin/env python3
"""
This is a math facts "game". It has a bunch of math facts, grouped by type, in an external pickle file. It asks you them, and it records whether you were right and how long you took. And when you press CTRL-C, it writes your results to another pickle file so you can pick up where you left off last time.

The next thing I'm going to add is multiple users
"""

import pickle
import os.path

import argv_parse

from . import Window, Fact, mathfactsdir, generate_facts

(player, *args), kwargs = argv_parse.parse()

player_path = os.path.join(mathfactsdir, f'{player.lower()}_facts.pickle')
try:
    with open(player_path, 'rb') as f:
        facts = pickle.load(f)
except FileNotFoundError:
    facts = generate_facts(player_path)


win = Window(facts)
win.root.mainloop()

if kwargs.get('record', True):
    with open(player_path, 'wb') as f:
        pickle.dump(facts, f)

# print(*map(repr, facts), sep='\t\t')