
EXIT_CODE = 99
ADD_CODE = 1
MUL_CODE = 2

def intcode(prog: list) -> list:
    counter = 0
    while prog[counter] != EXIT_CODE:
        if prog[counter] == ADD_CODE:
            prog[prog[counter + 3]] = prog[prog[counter + 1]] + prog[prog[counter + 2]]
        elif prog[counter] == MUL_CODE:
            prog[prog[counter + 3]] = prog[prog[counter + 1]] * prog[prog[counter + 2]]
        else:
            raise ValueError(f'Unexpected code {prog[counter]} at position {counter}.\n{prog=}')
        counter += 4
    return prog


def test_intcode():
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
        assert intcode(start_program) == end_program


def run_program(prog, noun, verb):
    prog = prog[:]
    prog[1] = noun
    prog[2] = verb
    return intcode(prog)[0]


PROG = [int(x) for x in open('inputs/day2.txt').read().split(',')]


def test_run_program():
    assert run_program(PROG, 12, 2) == 10566835


def main():
    for noun in range(100):
        for verb in range(100):
            if run_program(PROG, noun, verb) == 19690720:
                print(100 * noun + verb)
                return


if __name__ == '__main__':
    main()
