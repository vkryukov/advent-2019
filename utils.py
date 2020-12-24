# Input utilities
from math import *
from collections import Counter, namedtuple, defaultdict
import pickle
import requests
import typing


def Input(n, year=2020):
    n = int(n)
    filename = f'inputs/day{n:02}.txt'
    try:
        return open(filename).read()
    except FileNotFoundError:
        cookies = pickle.load(open('cookie', 'rb'))
        text = requests.get(f'https://adventofcode.com/{str(year)}/day/{n}/input', cookies=cookies).text
        open(filename, 'w').write(text)
        return text


def read_words(n): return [w for w in Input(n).split()]


def read_integers(n): return [int(w) for w in Input(n).split()]


def test_read_integers():
    num = read_integers(1)
    assert num[11] == 1514
    assert num[57] == 1713
    assert len(num) == 200


def read_lines(n): return [s for s in Input(n).split('\n') if s != '']


def all_lines(n): return [s for s in Input(n).split('\n')]


def count(iterable, fn=lambda x: x): return sum(fn(x) for x in iterable)


def prod(iterable):
    result = 1
    for x in iterable:
        result *= x
    return result

# def test_prod():
#     assert prod(range(1, 10)) == factorial(9)


def group_by(lst: typing.Iterable, /, key, sort_key=None) -> dict:
    """Groups LST elements by the value of KEY, and returns a dictionary mapping the value of key
    to all elements of LST with the given key. SORT_KEY, if set, sorts each of these lists."""
    d = defaultdict(list)
    for el in lst:
        d[key(el)].append(el)
    if sort_key:
        for el in d:
            d[el] = sorted(d[el], key=sort_key)
    return dict(d)


# def test_group_by():
#     lst = range(10)
#     assert group_by(lst, key=lambda x: x % 2) == {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
#     assert group_by(['mother', 'window', 'Mary', 'wash'], key=lambda s: s[0].lower()) == dict(
#         m=['mother', 'Mary'],
#         w=['window', 'wash']
#     )
#     assert group_by(['mother', 'wash', 'Mary', 'window'],
#                     key=lambda s: s[0].lower(),
#                     sort_key=len
#                     ) == dict(
#         m=['Mary', 'mother'],
#         w=['wash', 'window']
#     )
