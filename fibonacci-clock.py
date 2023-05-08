#!/usr/bin/env python3

from itertools import combinations
import random
from datetime import datetime, timedelta

import tkinter as tk

numbers = (5, 3, 2, 1, 1)  
MINUTES = '44' # blue
HOURS = '41'   # red
BOTH = '45'    # purple
NONE = '0'     # plain

n_parts = {
    0: {()}
}
for r in range(1, len(numbers)+1):
    for parts in combinations(numbers, r):
        s = sum(parts)
        # if s not in n_parts:
        #     n_parts[s] = set()
        n_parts.setdefault(s, set()).add(parts)

for n, parts in n_parts.items():
    n_parts[n] = list(parts)

# for n, parts in sorted(n_parts.items()):
#     print(f'{n:>2}: {parts!r}')

def parts(n, /):
    return random.choice(n_parts[n])

def print_time(time):
    # print(f'Fibonacci {time:%I:%M}')
    h_parts = list(parts(time.hour % 12))
    m_parts = list(parts(time.minute // 5))
    # print(h_parts, m_parts)
    boxes = []
    for n in numbers:
        if n in h_parts and n in m_parts:
            boxes.append((n, BOTH))
            h_parts.remove(n)
            m_parts.remove(n)
        elif n in h_parts:
            boxes.append((n, HOURS))
            h_parts.remove(n)
        elif n in m_parts:
            boxes.append((n, MINUTES))
            m_parts.remove(n)
        else:
            boxes.append((n, NONE))
    return ''.join(f'\x1b[{c}m {n} ' for n, c in boxes) + '\x1b[0m'

start = datetime.today()
twv_hrs = timedelta(hours=12)
"""
for _ in range(8):
    time = start + timedelta(
        hours=random.randint(1, 12),
        minutes=random.randrange(60)
    )
    guess = input(print_time(time) + '\nWhat time is it? ')
    guess = datetime.strptime(guess, '%I:%M').time()
    print(
        '\u2705' if (
            guess.hour in {time.hour, time.hour - 12}
            and guess.minute == time.minute - time.minute % 5
        )
        else f'{time:%I:%M}'
    )
"""

class FibonacciClock(object):
    sq_size = 20
    MINUTES = 'blue'
    HOURS = 'red'
    BOTH = 'purple'
    NONE = 'white'
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Fibonacci Clock')
        self.root.geometry(
            f'{self.sq_size * 8}x{self.sq_size * 5}'
        )

        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1, minsize=self.sq_size-2)
            if i < 5:
                self.root.rowconfigure(i, weight=1, minsize=self.sq_size-2)

        self.boxes = [
            (n, row_col, tk.Label(self.root, text=n, background='white'))
            for n, row_col in zip(numbers, [(0, 3), (2, 0), (0, 0), (0, 2), (1, 2)])
        ]
        for n, (row, col), box in self.boxes:
            box.grid(row=row, column=col, rowspan=n, columnspan=n, sticky='nsew', padx=4, pady=4)
        self.time_var = tk.StringVar()
        self.time = tk.Label(
            self.root,
            textvariable=self.time_var
        )
        self.time.grid(row=5, column=3, columnspan=2)

    def set_time(self, time):
        h_parts = list(parts(time.hour % 12))
        m_parts = list(parts(time.minute // 5))

        for n, _, box in self.boxes:
            if n in h_parts and n in m_parts:
                box.configure(background=self.BOTH)
                h_parts.remove(n)
                m_parts.remove(n)
            elif n in h_parts:
                box.configure(background=self.HOURS)
                h_parts.remove(n)
            elif n in m_parts:
                box.configure(background=self.MINUTES)
                m_parts.remove(n)
            else:
                box.configure(background=self.NONE)
        self.time_var.set(f'{time:%I:%M}')

    def random_time(self):
        time = start + timedelta(
            hours=random.randint(1, 12),
            minutes=random.randrange(60)
        )
        self.set_time(time)

    def now(self):
        self.set_time(datetime.now())

    def keep_time(self):
        now = datetime.now()
        self.set_time(now)
        wait = ((4 - now.minute % 5) * 60_000
                + (60 - now.second) * 1_000) - now.microsecond // 1000
        print(now, wait, self.root['width'], self.root['height'])
        self.root.after(
            wait,
            self.keep_time
        )


# for _ in range(8):
#     time = start + timedelta(
#         hours=random.randint(1, 12),
#         minutes=random.randrange(60)
#     )
#     guess = input(print_time(time) + '\nWhat time is it? ')
#     guess = datetime.strptime(guess, '%I:%M').time()
#     print(
#         '\u2705' if (
#             guess.hour in {time.hour, time.hour - 12}
#             and guess.minute == time.minute - time.minute % 5
#         )
#         else f'{time:%I:%M}'
#     )

def repeat():
    clock.random_time()
    clock.root.after(30_000, repeat)

clock = FibonacciClock()
clock.keep_time()
# clock.root.after(500, repeat)
clock.root.mainloop()