#!/usr/bin/env python3

import sys
import os
import time
from statistics import median, mode, quantiles
import csv

from namedtuple import NamedTuple, NamedList, NamedDict
from notify import notify
import argv_parse

if __name__ == '__main__':
    args, kwargs = argv_parse.parse()
else:
    args, kwargs = [], {}

battery_folder = '/sys/class/'
log_folder = os.path.expanduser('~/py/batt_log')


def num(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


def recurse_folder(abspath, keys_already):
    uevent = []
    if os.path.exists(f'{abspath}/uevent'):
        # It's a bunch of VAR_NAME=value
        # Battery attrs
        try:
            with open(f'{abspath}/uevent') as file:
                uevent = [line.strip().split('=', 1) for line in file]
        except PermissionError:
            pass
    keys_already.update(key for key, value in uevent)
    # Add will-be attrs from file list
    for direntry in os.scandir(abspath):
        if direntry.is_symlink():
            continue
        if direntry.is_file(follow_symlinks=False):
            if f'POWER_SUPPLY_{direntry.name.upper()}' in keys_already:
                continue
            if direntry.name == 'uevent':
                continue   # uevent is VAR_NAME=value. We already did it
            try:
                uevent.append(
                    [direntry.name, open(direntry.path).read().strip()]
                )
                keys_already.add(direntry.name)
            except OSError:
                pass
        elif direntry.is_dir(follow_symlinks=False):
            x, y = recurse_folder(direntry.path, keys_already)
            uevent.extend(x)
            keys_already.update(y)
    return uevent, keys_already


def sys_info(battery, folder='power_supply/'):
    batt_folder = ''.join((battery_folder, folder, battery))
    uevent, keys = recurse_folder(batt_folder, set())
    battery = NamedDict(
        {
            (key[13:].lower() if key.startswith('POWER_SUPPLY_') else key): (
                num(val) if isinstance(val, str) else val
            )
            for key, val in uevent
        }
    )
    battery.timestamp = round(time.time(), 1)
    if 'status' in battery:
        battery.charging = not battery.status == 'Discharging'
        battery.full = battery.status == 'Not charging'
    return battery


battery = sys_info('BAT0')
charger = sys_info('AC0')

header = ('timestamp', 'capacity', 'status', 'charging')
htypes = (float, int, lambda x: x, lambda x: x == 'True')
if kwargs.get('called-by') == 'crontab':
    with open(f'{log_folder}/power.csv', 'a') as file:
        csv.writer(file).writerow(battery.get(attr) for attr in header)


def at_percent(percent, x):
    x = sorted(x)
    if percent > 1:
        percent /= 100
    ind = percent * len(x)
    return x[round(ind)]


class BatteryLife(object):
    def __init__(self, status, length, start, end):
        self.status = status
        self.length = length
        self.start = start
        self.end = end

    def pretty(self):
        return f'{self.length/60:>2.0f}:{self.length%60:0>2.0f}:{(self.length%1)*60:0>2.0f}'

    def __str__(self, B='\x1b[1m'):
        p = '\x1b[0m'
        return f'Took {B}{self.pretty()}{p} of {B}{self.status.lower():<12}{p} to go from {B}{self.start:>2}%{p} to {B}{self.end:>2}%{p}.'


if kwargs.get('life'):

    def etype(row):
        return [htypes[i](row[i]) for i in range(len(row))]

    with open(f'{log_folder}/power.csv') as file:
        file.readline()
        data = [NamedDict(zip(header, etype(row))) for row in csv.reader(file)]
    timespaces = [
        round(data[i].timestamp - data[i - 1].timestamp, 1)
        for i in range(1, len(data))
    ]

    battery_lives = []
    len_data = len(data)
    graph_lines = []
    graph_xes = []
    for before, now, after, i in zip(
        data, data[1:], data[2:], range(1, len_data)
    ):
        avg_slice = timespaces[max(0, i - 10) : i + 10]
        max_dist = at_percent(80, avg_slice) * 1.1

        if now.status != before.status or not battery_lives:
            length = min(max_dist, after.timestamp - now.timestamp) / 60
            # The "min" constrains it to not more than the average
            battery_lives.append(
                BatteryLife(now.status, length, now.capacity, after.capacity)
            )
            graph_lines.append(
                NamedTuple(
                    charging=now.charging, line=[now.capacity, after.capacity]
                )
            )
            try:
                last_time = graph_xes[-1][-1]
            except IndexError:
                last_time = 0
            graph_xes.append(
                [
                    last_time + (max_dist / 3600),
                    last_time + (max_dist * 2 / 3600),
                ]
            )

        elif now.timestamp - before.timestamp <= max_dist:
            # Computer has (probably) been on since "before"
            # ELif because this was already accounted for when we added the NamedDict above
            battery_lives[-1].length += (now.timestamp - before.timestamp) / 60
            battery_lives[-1].end = now.capacity
            graph_lines[-1].line.append(now.capacity)
            graph_xes[-1].append(graph_xes[-1][-1] + (max_dist / 3600))
        else:
            # We are assuming the computer has been off.
            # It hasn't been using battery, but may have been charging.
            # Status == before.status, but computer has been off since "before"
            if now.charging:
                battery_lives[-1].length += (
                    now.timestamp - before.timestamp
                ) / 60
                battery_lives[-1].end = now.capacity
                graph_lines[-1].line.append(now.capacity)
                graph_xes[-1].append(
                    graph_xes[-1][-1]
                    + ((now.timestamp - before.timestamp) / 3600)
                )
    for life in battery_lives:
        print(life)

    assert len(graph_lines) == len(
        graph_xes
    ), f'{len(graph_lines)}, {len(graph_xes)}'
    import matplotlib.pyplot as plt

    plt.ylim(0, 100)
    plt.title('Battery Life')
    plt.grid()
    plt.xticks(range(0, round(graph_xes[-1][-1] + 1.5), 2))

    for line, x in zip(graph_lines, graph_xes):
        assert len(line.line) == len(x), f'{len(line.line)} != {len(x)}'
        plt.plot(x, line.line, 'g' if line.charging else 'r')
    plt.show()


if kwargs.get('called-by') == 'crontab' or kwargs.get('notify-level'):
    body = f'Your battery is at {battery.capacity}% and{" " if battery.charging else " not "}charging.'
    if battery.capacity >= 80 and battery.charging:
        notify(
            'Unplug your computer!',
            body,
            'full-battery',
            audio='bells',
            app_name='Battery',
        )
    elif battery.capacity <= 20 and not battery.charging:
        notify(
            'Plug in your computer!',
            body,
            'low-battery',
            audio='bells',
            app_name='Battery',
        )
