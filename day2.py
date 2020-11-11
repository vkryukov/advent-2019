
EXIT_CODE = 99
ADD_CODE = 1
MUL_CODE = 2

def intcode(prog: list) -> list:
    prog = prog[:]
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


def main():
    prog = [int(x) for x in open('day2.txt').read().split(',')]
    prog[1] = 12
    prog[2] = 2
    print(intcode(prog)[0])


if __name__ == '__main__':
    main()

