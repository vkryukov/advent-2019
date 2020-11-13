from intcode import Intcode
from utils import read_integers


def test_relative_mode():
    comp = Intcode([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])
    assert comp.run() == [
        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99
    ]
    assert Intcode([1102, 34915192, 34915192, 7, 4, 7, 99, 0]).run() == [1219070632396864]
    assert Intcode([104, 1125899906842624, 99]).run() == [1125899906842624]


def test_part1():
    assert Intcode(read_integers('inputs/day9.txt')).run([1]) == [2682107844]


def test_part2():
    assert Intcode(read_integers('inputs/day9.txt')).run([2]) == [34738]
