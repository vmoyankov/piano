#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
import time

import mido


onames = mido.get_output_names()
fluid = list(filter(lambda x: 'FLUID' in x, onames))

if len(fluid) == 0:
    print("Fluid synth not started")
    sys.exit(1)

fport = mido.open_output(fluid[0])
print(f'Connected to {fluid[0]}')


int_names = [
        'Прима',            # 0
        'малка Секунда',    # 1
        'голяма Секунда',   # 2
        'малка Терца',      # 3
        'голяма Терца',     # 4
        'Кварта',           # 5
        'увеличена Кварта', # 6
        'Квинта',           # 7
        'малка Секста',     # 8
        'голяма Секста',    # 9
        'малка Септима',    # 10
        'голяма Септима',   # 11
        'Октава',     # 12
        ]


def play_notes(notes, delay=0, duration=1.0, arp=False):
    for note in notes:
        msg=mido.Message('note_on', note=note)
        fport.send(msg)
        time.sleep(delay)
        if arp:
            msg=mido.Message('note_off', note=note)
            fport.send(msg)
    if not arp:
        time.sleep(duration)
        for note in notes:
            msg=mido.Message('note_off', note=note)
            fport.send(msg)


def play_random_intervals(n=10, choice=list(range(13)), base=None):
    for _ in range(n):
        if base is None:
            base_note = 48 + random.randrange(25)  # C3 - C5
        else:
            case_note = base
        interval = random.choice(choice)
        resp = ''
        while resp == '':
            play_notes((base_note, base_note+interval), delay=1.0, arp=True)
            resp = input(f"Press Enter for repeat, or {choice}: ")
        try:
            resp = int(resp)
            if resp == interval:
                print(f"Correct: {int_names[interval]}")
            else:
                print(f"                 ******* Wrong: {int_names[interval]}, not {int_names[resp]}")
        except ValueError:
            break
        time.sleep(1)


def print_intervals():
    for i, n in enumerate(int_names):
        print(i, n)

if __name__ == '__main__':
    print_intervals()
    play_random_intervals(100,[3,4])
