"""A math facts quiz game.
"""

import time
import random
import pickle
import os.path
from operator import add, sub, mul, truediv
from statistics import mean
from collections import deque
from functools import partial
import tkinter as tk

import audio

def intdiv(a, b, /):
    """Return a / b."""
    x = a / b
    assert int(x) == x
    return int(x)

class Fact(object):
    def __init__(self, i, oper, j, times=None, wrong_times=None, maxlen=None):
        self.operands = i, j
        self.i, self.j = i, j
        self.oper = oper
        match oper:
            case '+':
                self._oper = add
            case '-':
                self._oper = sub
            case 'x':
                self._oper = mul
            case '÷':
                self._oper = intdiv
            case _:
                raise ValueError(f'invalid operator {oper!r}')
        self._commutable = oper in '+x'
        self._double = (
            self.i == self.j
            or self.answer == self.i
            or self.answer == self.j
        )
        self.times = times or deque(maxlen=5)
        self.wrong_times = wrong_times or deque(maxlen=5)
        if maxlen is not None:
            self.times = deque(self.times, maxlen=maxlen)
            self.wrong_times = deque(self.wrong_times, maxlen=maxlen)
        self._last_str_order = tuple(self.operands)

    def __repr__(self):
        return f"Fact('{self.i}{self.oper}{self.j}', {self.difficulty:.3f}, times={list(self.times)}, wrong_times={list(self.wrong_times)})"

    def __str__(self):
        if self._commutable:
            opers = list(self.operands)
            random.shuffle(opers)
            self._last_str_order = tuple(opers)
            return f'{opers[0]}{self.oper}{opers[1]}='
        return f'{self.i}{self.oper}{self.j}='

    def __eq__(self, other):
        return self.operands == other.operands and self.oper == other.oper

    @property
    def answer(self):
        return self._oper(*self.operands)

    @property
    def difficulty(self):
        return (
            4 * (2 ** mean(self.wrong_times or [0]))
            + (0.8 * mean(self.times or [4]))
        ) * (2 if self._commutable else 1) * (2 if self._double else 1)


class Window(object):
    font = ('Ubuntu', 16)
    monospace = ('ubuntu-mono', 16)
    button_options = {'relief': tk.RAISED, 'borderwidth': 2}
    grid_options = {'sticky': 'nsew', 'padx': 2, 'pady': 2}

    def __init__(self, facts, **kwargs):
        self.facts = facts
        self.root = tk.Tk()
        self.root.title('MathFactsFast')
        self.root.geometry('200x300')
        self.root.config(background='white')
        # self.root.resizable(False, False)

        # Keypress handlers
        self.root.event_add(
            '<<numpress>>',
            *map(str, range(10)),
            *map(lambda n: f'<KeyPress-KP_{n}>', range(10))
        )
        self.root.bind_all('<<numpress>>', self.typed)
        self.root.bind_all('<KeyPress-Return>', self.check)
        self.root.bind_all('<KeyPress-KP_Enter>', self.check)
        self.root.bind_all('<KeyPress-BackSpace>', self.backspace)
        self.root.bind_all('<KeyPress-KP_Add>', self.backspace)
        self.root.bind_all('<Control-q>', lambda ev: self.root.quit())

        # Visuals
        for i in range(5):
            self.root.rowconfigure(i, weight=1, minsize=50)
            if i < 3:
                self.root.grid_columnconfigure(i, weight=1, minsize=40)

        self.screen_text = tk.StringVar(name='screen_text', value='0')
        self.screen_frame = tk.Frame(
            self.root,
            borderwidth=4,
            relief=tk.SUNKEN,
            background='#777'
        )
        self.screen_frame.grid(row=0, column=0, columnspan=3, **self.grid_options | {'padx': 6, 'pady': (6, 2)})
        self.screen = tk.Label(
            self.screen_frame,
            # justify=tk.RIGHT,
            anchor='e',
            textvariable=self.screen_text,
            font=self.monospace,
            # width=15,
            # height=2,
            background='white',
            borderwidth=15,
        )
        self.screen.pack(fill=tk.BOTH, expand=1)

        # Draw buttons
        self.buttons = []
        for i in range(10):
            row = 3 - (i - 1) // 3 # 1-3
            col = max(i - 1, 0) % 3 # 0-2
            cell_specific_options = {}
            if col == 0:
                cell_specific_options['padx'] = (6, 2)
            elif col == 2:
                cell_specific_options['padx'] = (2, 6)
            if row == 4:
                cell_specific_options['pady'] = (2, 6)
            self.buttons.append(
                tk.Button(
                    self.root,
                    command=partial(self.clicked, str(i)),
                    text=str(i),
                    font=self.font,
                    borderwidth=2,
                )
            )
            self.buttons[-1].grid(
                row=row,
                column=col,
                **self.grid_options | cell_specific_options
            )

        self.enter = tk.Button(
            self.root,
            command=self.check,
            text='=',
            font=self.font,
            borderwidth=2,
        )
        self.enter.grid(row=4, column=2, **self.grid_options | {'padx': (2, 6), 'pady': (2, 6)})

        font = list(self.font)
        font[1] -= 4
        self.backspace_button = tk.Button(
            self.root,
            command=self.backspace,
            text='\u21cd',
            font=font,
            borderwidth=2
        )
        self.backspace_button.grid(
            row=4,
            column=1,
            **self.grid_options | {'pady': (2, 6)}
        )

        self.typed_numbers = ''
        self.root.after(1000, self.set_problem)

        # self._problem = None
        # self.problem_details = None

    def clicked(self, number):
        # print(number, 'clicked')
        self.typed_numbers += number
        self.screen_text.set(self.screen_text.get() + number)

    def typed(self, event):
        # print(f'Typed: {event.keysym=}, {event.keycode=}, {event.keysym_num=}, {event=}')
        self.clicked(event.keysym[-1])

    def backspace(self, event=None):
        if not self.typed_numbers: return
        self.typed_numbers = self.typed_numbers[:-1]
        self.screen_text.set(self.screen_text.get()[:-1])

    def set_problem(self):
        self.screen.config(background='white')
        self.fact = random.choices(self.facts, [fact.difficulty for fact in self.facts])[0]
        self.typed_numbers = ''
        self.screen_text.set(str(self.fact))
        self.asked_time = time.perf_counter()

    def check(self, event=None):
        try:
            self.fact.times.append(time.perf_counter() - self.asked_time)
        except TypeError:
            pass
        else:
            self.asked_time = None
            number = int(self.typed_numbers)
            if number == self.fact.answer:
                self.screen.config(background='green')
                audio.play('doo-d-ling', sync=False)
                self.fact.wrong_times.append(False)
                self.root.after(1000, self.set_problem)
            else:
                self.screen.config(background='red')
                audio.play('beep', sync=False)
                self.fact.wrong_times.append(True)
                self.screen_text.set(str(self.fact) + str(self.fact.answer))
                self.root.after(3000, self.set_problem)


mathfactsdir = os.path.dirname(__file__)


def main():
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

def generate_facts(path):
    opers = '+-x'
    facts = []
    for i in range(1, 13):
        for j in range(1, 13):
            if j > i:
                break
            facts.append(Fact(i, '+', j))
            facts.append(Fact(i+j, '-', i))
            if j != i: facts.append(Fact(i+j, '-', j))

            facts.append(Fact(i, 'x', j))
            facts.append(Fact(i*j, '÷', i))
            if j != i: facts.append(Fact(i*j, '÷', j))
            # for oper in opers:
            #     facts.append(Fact(i, oper, j))
    with open(path, 'wb') as f:
        pickle.dump(facts, f)
    return facts