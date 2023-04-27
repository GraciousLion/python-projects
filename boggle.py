#!/usr/bin/env python3

from itertools import chain

import numpy as np

def _valid(word):
    return word.islower() and word.isascii() and len(word) < 17

with open('/usr/share/dict/words') as f:
    words = {l for l in f.read().split('\n') if _valid(l)}
with open('data/merriam-webster-words') as f:
    words.update(l for l in f.read().split('\n') if _valid(l))

def input_board():
    print('Enter the board:')
    board = [
        m.split()
        if len(m := input().lower()) != 4
        else list(m)
        for i in range(4)
    ]
    assert all(len(r) == 4 for r in board), f'Invalid board: {board}'

    board = np.array(board)
    # print(repr(board))
    # board = np.array([['a', 'e', 'k', 'h'],
    #                  ['l', 'l', 'e', 's'],
    #                  ['i', 't', 'a', 'c'],
    #                  ['t', 'g', 'r', 'i']], dtype='<U1')
    return board


def neighbors(board: np.ndarray, pos: tuple[int, int]) -> list[str]:
    changes = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for change in changes:
        new_pos = pos[0] + change[0], pos[1] + change[1]
        if (
            -1 < new_pos[0] < board.shape[0]
            and -1 < new_pos[1] < board.shape[1]
        ):
            yield board[new_pos], new_pos, change

class String:
    values = {
        1:  0,
        2:  0,
        3:  1,
        4:  1,
        5:  2,
        6:  3,
        7:  5,
        8: 11,
        9: 11,
        10: 11,
        12: 11,
        13: 11,
        14: 11,
        15: 11,
        16: 11,
    }
    arrows = {
        ( 0, -1): '\u2190', # left
        (-1,  0): '\u2191', # up
        ( 0,  1): '\u2192', # right
        ( 1,  0): '\u2193', # down
        (-1, -1): '\u2196', # up left
        (-1,  1): '\u2197', # up right
        ( 1,  1): '\u2198', # down right
        ( 1, -1): '\u2199', # down left
    }
    def __init__(self, board, chars=(), tiles=(), changes=()):
        self.board = board
        self.chars = tuple(chars)
        self.tiles = tuple(tiles)
        self.changes = tuple(changes)
        assert len(self.chars) == len(self.tiles), ('Chars and tiles unequal:'
                                         f' {self.chars=!r}, {self.tiles=}')
        self.word = ''.join(self.chars)
        self.exists = self.word in words
        self.points = self.values[len(self)]

    def __str__(self):
        return self.word

    def __repr__(self):
        repr_board = repr(self.board).replace('\n', '\n    ')
        return f'String(\n    np.{repr_board},\n    {self.chars!r},\n    {self.tiles!r}\n)'

    def __len__(self):
        return len(self.word)

    def __hash__(self):
        return hash(self.word)

    def __gt__(self, other):
        return (-self.points, self.word) > (-other.points, other.word)

    def __eq__(self, other):
        return self.word == other.word

    '''
    def location(self):
        string = []
        for r, row in enumerate(self.board):
            string.append([])
            for c, letter in enumerate(row):
                if (r, c) == self.tiles[0]:
                    string[-1].append(f'\x1b[1;32m{letter.upper()}\x1b[0m')
                elif (r, c) == self.tiles[-1]:
                    string[-1].append(f'\x1b[1;35m{letter.upper()}\x1b[0m')
                elif (r, c) in self.tiles:
                    string[-1].append(f'\x1b[1m{letter.upper()}\x1b[0m')
                else:
                    string[-1].append(letter.upper())
        return '\n'.join(''.join(row) for row in string) + '\n' + ', '.join(map(lambda p: str((p[0]+1, p[1]+1)), self.tiles))
    '''

    def location(self):
        board = [
            [
                self.board[row // 2, col // 3].upper()
                if row % 2 == 0 and col % 3 == 0
                else ' '
                for col in range(10)
            ]
            for row in range(7)
        ]
        one_r, one_c = self.tiles[0]
        board[one_r * 2][one_c * 3] = f'\x1b[1;32m{self.chars[0].upper()}\x1b[0m'
        for start, change in zip(self.tiles, self.changes):
            arrow_r, arrow_c = start[0] * 2 + change[0], start[1] * 3 + change[1] * 2
            if change[1] == 1:
                arrow_c -= 1
            arrow = self.arrows[change]
            board[arrow_r][arrow_c] = arrow
        return '\n'.join(''.join(row) for row in board)

    def print_location(self):
        print(self.location())

    def define(self):
        r = requests.get(f'https://www.merriam-webster.com/dictionary/{self.word}')
        if not r:
            print(r.status_code, r.reason)
            print('Word does not exist.')
            self.exists = False
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        word = soup.find(class_='hword').string.strip()
        if word != self.word:
            print('Word is misspelled, plural, or past tense; defining', word)
        defs = soup.find(class_='vg').find_all(class_='vg-sseq-entry-item', limit=4)
        template = """{n} : {definition}{example}"""
        for n, defin in enumerate(defs, 1):
            for upper in defin.find_all(class_='text-uppercase'):
                if upper.string: upper.string = upper.string.upper()
            definition = ''.join(
                str(s)
                for i, s in enumerate(defin.find(class_='dtText').strings)
                if i != 0
            )
            # try:
            #     example = 
            # except AttributeError:
            #     example = ''
            # else:
            #     example = 
            example = defin.find(class_='sub-content-thread')
            if example is None:
                example = ''
            else:
                example = '\n    \x1b[3m' + ''.join(example.strings) + '\x1b[0m'
            print(template.format(
                n=n,
                definition=definition,
                example=example
            ))

    def add(self, pos, change):
        return String(
            self.board,
            self.chars + (self.board[pos],),
            self.tiles + (pos,),
            self.changes + (change,),
        )

    def spawn(self):
        could_be = [w for w in words if w.startswith(self.word) and self.word != w]
        if not could_be:
            return (None for none in [])
        for letter, pos, change in neighbors(self.board, self.tiles[-1]):
            if pos in self.tiles:
                continue
            string = self.add(pos, change)
            if any(w.startswith(string.word) for w in could_be):
                yield string


if __name__ == '__main__':
    import webbrowser

    import requests
    from bs4 import BeautifulSoup

    board = input_board()

    last_spawned = [
        String(board, (char,), [(r, c)])
        for r, row in enumerate(board)
        for c, char in enumerate(row)
    ]

    valid_words = {}
    while last_spawned:
        last_spawned = list(chain(*[string.spawn() for string in last_spawned]))
        if last_spawned and len(last_spawned[0]) > 2:
            valid_words.update({w.word: w for w in last_spawned if w.exists})

    print(f'\nFound {len(valid_words)} words, for {sum(w.points for w in valid_words.values())} points:')
    print(*sorted(valid_words.values()), sep='\t')


    USAGE = '''Usage:
             \r  def WORD      define WORD
             \r  show WORD     show location of WORD on board
             \r  open WORD     open definition of WORD in browser'''
    try:
        while True:
            # TO DO: Potentially rework to use match instead
            command = input('> ').lower()
            if command == 'q':
                break
            if command.count(' ') != 1:
                print(USAGE)
                continue
            command, word = command.split(' ')
            if command not in {'def', 'show', 'open'}:
                print(USAGE)
                continue
            try:
                word = valid_words[word]
            except KeyError:
                print('Word not found.')
            else:
                if command == 'def':
                    word.define()
                elif command == 'show':
                    word.print_location()
                elif command == 'open':
                    webbrowser.open(f'https://www.merriam-webster.com/dictionary/{word.word}')
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print('\r      \r', end='')
