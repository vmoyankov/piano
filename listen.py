#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
import time

import mido


names = mido.get_output_names()
piano = list(filter(lambda x: 'FP-30' in x, names))

if len(piano) == 0:
    print("The piano is not connected")
    sys.exit(1)

port = mido.open_ioport(piano[0])
print(f'Connected to {piano[0]}')


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

Major = [0,2,4,5,7,9,11]
Minor = [0,2,3,5,7,8,10]

def play_notes(notes, delay=0, duration=1.0, arp=False, channel=1):
    for note in notes:
        msg=mido.Message('note_on', note=note, channel=channel)
        port.send(msg)
        time.sleep(delay)
        if arp:
            msg=mido.Message('note_off', note=note, channel=channel)
            port.send(msg)
    if not arp:
        time.sleep(duration)
        for note in notes:
            msg=mido.Message('note_off', note=note, channel=channel)
            port.send(msg)


def guess_note(choice=Major+[12]):
    base_n = 60 # C4
    old = 0
    k = 0
    while True:
        while abs(k - old) < 3:
            k = random.choice(choice)
        old = k
        #o = random.choice((-12, 0 , 12))
        o = 0
        n = base_n + o + k
        print(o, k)
        play_notes((n,))
        while True:
            m = port.receive()
            if m.type == 'note_on':
                inote = m.note
                if inote == 21:
                    return
                if inote == 22:
                    break
                if inote == 23:
                    play_notes((n,))
                    continue
                if inote == n:
                    print("OK")
                    time.sleep(0.2)
                    play_notes((60,), channel=9, duration=0.3)
                    break
                else:
                    a = inote % 12
                    print(f"Error:{k} -> {a}")

        time.sleep(2)


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
    guess_note()
