from typing import Optional


class Intcode:
    """Represents an Intcode computer"""

    EXIT_CODE = 99
    ADD_CODE = 1
    MUL_CODE = 2

    def __init__(self, program):
        self._program = program
        self._memory = program[:]

    @staticmethod
    def op_and_params(instruction):
        op = instruction % 100
        modes = []
        instruction //= 100
        while instruction > 0:
            modes.append(instruction % 10)
            instruction //= 10
        return op, modes

    def values(self, counter, count, modes):
        """Given the memory counter and params, return COUNT values according"""
        return [self._memory[self._memory[counter+i]]
                if (i >= len(modes) or modes[i] == 0)
                else self._memory[counter+i]
                for i in range(1, count+1)]

    def run(self, input: Optional[list] = None) -> list:
        """Runs Intcode on a given input, producing given output."""
        output = []
        input_counter = 0
        self._memory = self._program[:]
        counter = 0
        while self._memory[counter] != Intcode.EXIT_CODE:
            op, modes = Intcode.op_and_params(self._memory[counter])
            if op == Intcode.ADD_CODE:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = x + y
                counter += 4
            elif op == Intcode.MUL_CODE:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = x * y
                counter += 4
            else:
                raise ValueError(f'Unexpected code {self._memory[counter]} at position {counter}.\n{self._memory=}')
        return output

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
