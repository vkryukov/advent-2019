"""
Implementation of Intcode computer.
"""

from typing import Optional


class Intcode:
    """Represents an Intcode computer"""

    EXIT = 99
    ADD = 1
    MUL = 2
    READ = 3
    WRITE = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS = 7
    EQUALS = 8

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
        return [(self._memory[self._memory[counter + i + 1]]
                 if (i >= len(modes) or modes[i] == 0)
                 else self._memory[counter + i + 1])
                for i in range(count)]

    def run(self, input: Optional[list] = None, /, memory_reset=True) -> list:
        """Runs Intcode on a given input, producing given output."""
        output = []
        if memory_reset:
            self._memory = self._program[:]
        counter = 0
        while self._memory[counter] != Intcode.EXIT:
            op, modes = Intcode.op_and_params(self._memory[counter])
            if op == Intcode.ADD:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = x + y
                counter += 4
            elif op == Intcode.MUL:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = x * y
                counter += 4
            elif op == Intcode.READ:
                self._memory[self._memory[counter + 1]] = input.pop(0)
                counter += 2
            elif op == Intcode.WRITE:
                x, = self.values(counter, 1, modes)
                output.append(x)
                counter += 2
            elif op == Intcode.JUMP_IF_TRUE:
                x, y = self.values(counter, 2, modes)
                if x != 0:
                    counter = y
                else:
                    counter += 3
            elif op == Intcode.JUMP_IF_FALSE:
                x, y = self.values(counter, 2, modes)
                if x == 0:
                    counter = y
                else:
                    counter += 3
            elif op == Intcode.LESS:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = (1 if x < y else 0)
                counter += 4
            elif op == Intcode.EQUALS:
                x, y = self.values(counter, 2, modes)
                self._memory[self._memory[counter + 3]] = (1 if x == y else 0)
                counter += 4
            else:
                raise ValueError(f'Unexpected code {self._memory[counter]} at position {counter}.\n{self._memory=}')
        return output

    @property
    def memory(self):
        """Return the state of the memory after the run."""
        return self._memory


