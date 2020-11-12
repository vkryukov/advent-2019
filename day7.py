import itertools

from intcode import Intcode
from utils import read_integers


class Amplifiers:
    def __init__(self, program: list):
        self.A = Intcode(program)
        self.B = Intcode(program)
        self.C = Intcode(program)
        self.D = Intcode(program)
        self.E = Intcode(program)

    def run(self, phases: (list, tuple)) -> int:
        a, b, c, d, e = phases
        b_in, = self.A.run([a, 0])
        c_in, = self.B.run([b, b_in])
        d_in, = self.C.run([c, c_in])
        e_in, = self.D.run([d, d_in])
        out, = self.E.run([e, e_in])
        return out

    def find_best_phase(self) -> tuple:
        best = max([(phases, self.run(phases)) for phases in itertools.permutations(range(5))],
                   key=lambda x: x[-1])
        return best


def test_amplifiers():
    assert Amplifiers([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]).run([4, 3, 2, 1, 0]) == 43210
    assert Amplifiers(
        [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]).run(
        [0, 1, 2, 3, 4]) == 54321
    assert Amplifiers(
        [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31,
         31, 4, 31, 99, 0, 0, 0]).run(
        [1, 0, 4, 3, 2]) == 65210


def test_find_best_phase():
    assert Amplifiers(
        [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    ).find_best_phase() == ((4, 3, 2, 1, 0), 43210)
    assert Amplifiers(
        [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    ).find_best_phase() == ((0, 1, 2, 3, 4), 54321)
    assert Amplifiers(
        [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31,
         31, 4, 31, 99, 0, 0, 0]
    ).find_best_phase() == ((1, 0, 4, 3, 2), 65210)


def part1():
    amp = Amplifiers(read_integers('inputs/day7.txt'))
    print(amp.find_best_phase())


if __name__ == '__main__':
    part1()