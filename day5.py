from typing import Optional


class Intcode:
    """Represents an Intcode computer"""

    EXIT_CODE = 99
    ADD_CODE = 1
    MUL_CODE = 2

    def __init__(self, program):
        self._program = program
        self._memory = program[:]

    def run(self, input: Optional[list] = None) -> list:
        """Runs Intcode on a given input, producing given output."""
        self._memory = self._program[:]
        counter = 0
        while self._memory[counter] != Intcode.EXIT_CODE:
            if self._memory[counter] == Intcode.ADD_CODE:
                self._memory[self._memory[counter + 3]] = self._memory[self._memory[counter + 1]] + self._memory[self._memory[counter + 2]]
            elif self._memory[counter] == Intcode.MUL_CODE:
                self._memory[self._memory[counter + 3]] = self._memory[self._memory[counter + 1]] * self._memory[self._memory[counter + 2]]
            else:
                raise ValueError(f'Unexpected code {self._memory[counter]} at position {counter}.\n{self._memory=}')
            counter += 4

    @property
    def memory(self):
        """Return the state of the memory after the run."""
        return self._memory


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
        comp = Intcode(start_program)
        comp.run()
        assert comp.memory == end_program
