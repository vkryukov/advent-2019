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
        self._memory = self._input = None

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

    def reset(self):
        self._memory = self._program[:]
        self.pos = 0

    def run_until_output(self) -> Optional[int]:
        """Runs Intcode on a given input, producing given output."""
        while self._memory[self.pos] != Intcode.EXIT:
            op, modes = Intcode.op_and_params(self._memory[self.pos])
            if op == Intcode.ADD:
                x, y = self.values(self.pos, 2, modes)
                self._memory[self._memory[self.pos + 3]] = x + y
                self.pos += 4
            elif op == Intcode.MUL:
                x, y = self.values(self.pos, 2, modes)
                self._memory[self._memory[self.pos + 3]] = x * y
                self.pos += 4
            elif op == Intcode.READ:
                self._memory[self._memory[self.pos + 1]] = self._input.pop(0)
                self.pos += 2
            elif op == Intcode.WRITE:
                x, = self.values(self.pos, 1, modes)
                self.pos += 2
                return x
            elif op == Intcode.JUMP_IF_TRUE:
                x, y = self.values(self.pos, 2, modes)
                if x != 0:
                    self.pos = y
                else:
                    self.pos += 3
            elif op == Intcode.JUMP_IF_FALSE:
                x, y = self.values(self.pos, 2, modes)
                if x == 0:
                    self.pos = y
                else:
                    self.pos += 3
            elif op == Intcode.LESS:
                x, y = self.values(self.pos, 2, modes)
                self._memory[self._memory[self.pos + 3]] = (1 if x < y else 0)
                self.pos += 4
            elif op == Intcode.EQUALS:
                x, y = self.values(self.pos, 2, modes)
                self._memory[self._memory[self.pos + 3]] = (1 if x == y else 0)
                self.pos += 4
            else:
                raise ValueError(f'Unexpected code {self._memory[self.pos]} at position {self.pos}.\n{self._memory=}')
        return None

    def run(self, inp: Optional[list] = None) -> list:
        self.reset()
        self._input = inp[:] if inp else []
        output = []
        while (o := self.run_until_output()) is not None:
            output.append(o)
        return output

    @property
    def memory(self):
        """Return the state of the memory after the run."""
        return self._memory


