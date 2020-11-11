from utils import read_integers
from intcode import Intcode

COMP = Intcode(read_integers('inputs/day5.txt'))


def test_part1():
    assert COMP.run([1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 13787043]


def test_part2():
    assert COMP.run([5]) == [3892695]
