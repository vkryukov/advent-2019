from intcode import Intcode
from utils import read_integers

PROGRAM = read_integers('inputs/day2.txt')


def run_program(noun, verb):
    prog = PROGRAM[:]
    prog[1] = noun
    prog[2] = verb
    comp = Intcode(prog)
    comp.run()
    return comp._memory[0]


def test_part1():
    assert run_program(12, 2) == 10566835


def test_part2():
    assert run_program(23, 47) == 19690720


def main():
    for noun in range(100):
        for verb in range(100):
            if run_program(noun, verb) == 19690720:
                print(100 * noun + verb)
                return


if __name__ == '__main__':
    main()
