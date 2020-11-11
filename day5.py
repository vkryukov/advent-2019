from typing import Optional


class Intcode:
    """Represents an Intcode computer"""

    EXIT_CODE = 99
    ADD_CODE = 1
    MUL_CODE = 2
    READ_INPUT_CODE = 3
    WRITE_OUTPUT_CODE = 4

    def __init__(self, program):
        self._program = program[:]
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
        return [self._memory[self._memory[counter+i+1]]
                if (i >= len(modes) or modes[i] == 0)
                else self._memory[counter+i+1]
                for i in range(count)]

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
            elif op == Intcode.READ_INPUT_CODE:
                x, = self.values(counter, 1, modes)
                self._memory[x] = input[input_counter]
                input_counter += 1
                counter += 2
            elif op == Intcode.WRITE_OUTPUT_CODE:
                x, = self.values(counter, 1, modes)
                output.append(self._memory[x])
            else:
                raise ValueError(f'Unexpected code {self._memory[counter]} at position {counter}.\n{self._memory=}')
        return output

    @property
    def memory(self):
        """Return the state of the memory after the run."""
        return self._memory


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
