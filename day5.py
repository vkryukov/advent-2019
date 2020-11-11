from utils import read_integers
from intcode import Intcode


def test_intcode_basic_program():
    for start_program, end_program in [
        [[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
         [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]],
        [[1, 0, 0, 0, 99],
         [2, 0, 0, 0, 99]],
        [[2, 3, 0, 3, 99],
         [2, 3, 0, 6, 99]],
        [[2, 4, 4, 5, 99, 0],
         [2, 4, 4, 5, 99, 9801]],
        [[1, 1, 1, 4, 99, 5, 6, 0, 99],
         [30, 1, 1, 4, 2, 5, 6, 0, 99]],
    ]:
        comp = Intcode(start_program)
        comp.run()
        assert comp.memory == end_program


def test_another_simple_program():
    comp = Intcode([1002, 4, 3, 4, 33])
    comp.run()
    assert comp.memory == [1002, 4, 3, 4, 99]
    comp = Intcode([1101, 100, -1, 4, 0])
    comp.run()
    assert comp.memory == [1101, 100, -1, 4, 99]


def test_read_input():
    comp = Intcode([103, 9, 103, 10, 2, 9, 10, 8, 0, 0, 0])
    comp.run([33, 3])
    assert comp.memory == [103, 9, 103, 10, 2, 9, 10, 8, 99, 33, 3]


def test_day5_program():
    comp = Intcode(read_integers('inputs/day5.txt'))
    diagnostic = comp.run([1])
    assert diagnostic == [0, 0, 0, 0, 0, 0, 0, 0, 0, 13787043]


def test_comparisons():
    assert Intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]).run([8]) == [1]
    assert Intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]).run([7]) == [0]

    assert Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run([6]) == [1]
    assert Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run([8]) == [0]
    assert Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run([10]) == [0]

    assert Intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99]).run([8]) == [1]
    assert Intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99]).run([7]) == [0]

    assert Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run([6]) == [1]
    assert Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run([8]) == [0]
    assert Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run([10]) == [0]


def test_jumps():
    assert Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]).run([0]) == [0]
    assert Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]).run([1]) == [1]
    assert Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]).run([-2]) == [1]

    assert Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]).run([0]) == [0]
    assert Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]).run([42]) == [1]
    assert Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]).run([-57]) == [1]


def test_large_example():
    comp = Intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
    assert comp.run([-42]) == [999]
    assert comp.run([8]) == [1000]
    assert comp.run([57]) == [1001]


def test_diagnostic2():
    comp = Intcode(read_integers('inputs/day5.txt'))
    diagnostic = comp.run([5])
    assert diagnostic == [3892695]
