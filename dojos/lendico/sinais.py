#!/usr/bin/env python3

import sys

def search(query, data):
    query = query.replace('-',' ')
    words = set(query.upper().split())
    for code, char, name in data:
        name = name.replace('-',' ')
        if words <= set(name.split()):
            yield f'{code}\t{char}\t{name}'

def reader():
    with open('UnicodeData.txt') as _file:
        for line in _file:
            code, name = line.split(';')[:2]
            char = chr(int(code, 16))
            yield f'U+{code}', char, name


def main(*words):
    if len(words) < 1:
        print("Please provide one word or more", file=sys.stderr)
        return

    query = ' '.join(words)
    index = -1

    for index, line in enumerate(search(query, reader())):
        print(line)

    if index == -1:
        print("No results", file=sys.stderr)

if __name__ == "__main__":
    main(*sys.argv[1:])
