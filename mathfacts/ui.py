#!/usr/bin/env python3
"""Manages tkinter UI.
"""

import time
from functools import partial
import tkinter as tk


class Window(object):
    font = ('Ubuntu', 16)
    monospace = ('ubuntu-mono', 16)

    def __init__(self, **kwargs):
        self.root = tk.Tk()
        self.root.title('MathFactsFast')
        self.root.geometry('225x300')
        # self.root.resizable(False, False)
        for i in range(5):
            self.root.rowconfigure(i, weight=1, minsize=50)
            if i < 3:
                self.root.columnconfigure(i, weight=1, minsize=50)

        self.screen_text = tk.StringVar(name='screen_text', value='0')
        self.screen = tk.Label(
            self.root,
            # justify=tk.RIGHT,
            anchor='e',
            textvariable=self.screen_text,
            font=self.monospace,
            # width=15,
            # height=2,
            background='#999',
            borderwidth=10,
        )
        self.screen.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=2)

        # Draw buttons
        self.buttons = []
        for i in range(10):
            self.buttons.append(
                tk.Button(
                    self.root,
                    command=partial(self.clicked, str(i)),
                    text=str(i),
                    # width=5,
                    # height=2,
                    font=self.font,
                    borderwidth=2,
                )
            )
            self.buttons[-1].grid(
                row=3 - (i - 1) // 3,
                column=max(i - 1, 0) % 3,
                sticky='nsew',
                padx=1,
                pady=1,
            )

        self.enter = tk.Button(
            self.root,
            command=self.check,
            text='=',
            font=self.font,
            borderwidth=2,
        )
        self.enter.grid(row=4, column=1, columnspan=2, sticky='nsew')

        self._problem = None
        self.problem_details = None

    def clicked(self, number):
        print(number, 'clicked')
        self.typed_numbers += number

    def set_problem(self):
        self.asked_time = time.perf_counter()

    def check(self):
        number = int(self.typed_numbers)
        if number == self.problem_details['answer']:
            self.root.config(background='green')
            self.problem_details['wrong_times'].append(False)
        else:
            self.root.config(background='red')
            self.problem_details['wrong_times'].append(True)
        self.root.after(1000, self.set_problem)

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self.problem_details = value[1]
            value = value[0]
        self._problem = value
        self.screen_text.set(f'{value[0]}{value[1]}{value[2]}=')
        self.typed_numbers = ''


if __name__ == '__main__':
    ui = Window()
    ui.root.mainloop()
