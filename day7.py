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

    def find_best_phase(self, inputs=range(5)) -> tuple:
        best = max([(phases, self.run(phases)) for phases in itertools.permutations(inputs)],
                   key=lambda x: x[-1])
        return best


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


class FeedbackAmplifiers(Amplifiers):
    def run(self, phases: (list, tuple)) -> int:
        a, b, c, d, e = phases
        self.A.reset([a])
        self.B.reset([b])
        self.C.reset([c])
        self.D.reset([d])
        self.E.reset([e])
        a_in = 0
        while True:
            self.A.append_input(a_in)
            b_in = self.A.run_until_output()
            if b_in is None:
                return a_in
            self.B.append_input(b_in)
            c_in = self.B.run_until_output()
            self.C.append_input(c_in)
            d_in = self.C.run_until_output()
            self.D.append_input(d_in)
            e_in = self.D.run_until_output()
            self.E.append_input(e_in)
            a_in = self.E.run_until_output()


def test_feedback_amplifiers():
    assert FeedbackAmplifiers([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                               27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
                              ).find_best_phase(range(5, 10)) == ((9, 8, 7, 6, 5), 139629729)
    assert FeedbackAmplifiers([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                               -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                               53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
                              ).find_best_phase(range(5, 10)) == ((9, 7, 8, 5, 6), 18216)


def part2():
    amp = FeedbackAmplifiers(read_integers('inputs/day7.txt'))
    print(amp.find_best_phase(range(5, 10)))


if __name__ == '__main__':
    part2()
