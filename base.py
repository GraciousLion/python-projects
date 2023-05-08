#!/usr/bin/env python3

MAX_DECIMAL_PLACES = 20

import logging
from logging import debug, info, warning, critical

logging.basicConfig(
    format='{levelname:<6} \x1b[4mline {lineno}\x1b[0m : \x1b[3m{msg}\x1b[0m',
    style='{',
    level=30,
)

numerals = tuple(
    '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)


def base(x, from_base, to_base=10):
    x = x if isinstance(x, str) else str(x)
    negative = x[0] == '-'
    x = x.replace('-', '')
    if x == '0':
        return 0.0 if to_base == 10 else '0'
    if from_base == to_base:
        return x if to_base != 10 else float(x)
    new = ''
    total = 0
    nplace = from_base ** (len(x.split('.')[0]) - 1)

    def oplace():
        if '.' not in new:
            return to_base ** len(new)
        return to_base ** (-(len(new.split('.')[0]) + 1))

    def next_place_val():
        if total >= 1:
            return oplace() * to_base
        return oplace() / to_base

    # Figure out value of x
    if from_base == 10:
        total = float(x)
    else:
        for char in x:
            if char in {'.', '-'}:
                continue
            val = numerals.index(char)
            if val >= from_base:
                raise ValueError(
                    'invalid literal for base ' f'{from_base} {x!r}'
                )
            total += val * nplace
            # debug(f'char {char} {val} {total} nplace {nplace} {new!r} oplace {oplace()}')
            nplace /= from_base
    info(f'value of b{from_base} {x} ~= {total:.6f}')
    if to_base == 10:
        if not negative:
            return total
        else:
            return -total

    # Building "new" string
    while total > 0 and len(new.split('.')[0]) <= MAX_DECIMAL_PLACES:
        if total < 1 and '.' not in new:
            if not new:
                new = '0'
            new = f'.{new}'
        debug(
            f'{total} {new!r} oplace {oplace():.4f} next val "{next_place_val():.4f}"'
        )
        if total < oplace():
            if total < 1:
                new = f'0{new}'
                # else: new += '0'
                continue
        if total < 1:
            dig_val = total // oplace()
        else:
            dig_val = (total % next_place_val()) / oplace()
        dig_val = int(dig_val)
        info(
            f'dig_val {dig_val} total {total} next val {next_place_val()} amount {dig_val*oplace()}'
        )
        # if dig_val == to_base:
        #     if total >= 1: new += '0'
        #     else: new = f'0{new}'
        #     continue
        prev_tot = total
        total -= dig_val * oplace()
        num = numerals[int(dig_val)]
        if prev_tot < 1:
            new = f'{num}{new}'
        else:
            new += num
        debug(
            f'{total:.6f} appended {dig_val} {new!r} '
            f'oplace {oplace():.5f} {next_place_val():.5f} '
            f'{total > 0} {len(new.split(".")[0]) <= MAX_DECIMAL_PLACES}'
        )
    if not new:
        new = '0'
    elif new.endswith('.'):
        new += '0'
    if new.startswith('.'):
        new = f'0{new}'
    if negative:
        new += '-'
    return new[::-1]


if __name__ == '__main__':
    import argv_parse

    args, kwargs = argv_parse.parse()
    if args or kwargs:
        print(repr(base(*args, **kwargs)))
    else:
        for i in range(40):
            i = i / 5
            b3 = base(i, 10, 3)
            print(f'{i:>2} to b3 -> {b3}\x1b[0m')
            b10 = base(b3, 3)
            if str(i) not in {str(round(b10, 9)), f'{b10}.0'}:
                critical(
                    f'after converting \x1b[1m{i}\x1b[22m to b3 and back again, is \x1b[1m{b10:.9f}'
                )
            # print(f'{b3:>7} to b10 -> (should be {i}) {b10}')
            # if b10 != str(i):
            #     warning(f'after converting {i} to b3 and back again, is {b10}')


# base('10', 2, 10) == '2'
# base('4', 10, 2) == '100'
