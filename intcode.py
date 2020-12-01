"""
Implementation of Intcode computer.
"""

from typing import Optional

from utils import read_integers


MEMORY_SIZE = 1_000_000


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
    ADJUST_REL_BASE = 9

    def __init__(self, program):
        self._program = program[:]
        self._memory = [0] * MEMORY_SIZE
        self.pos = self.relative_base = None
        self._input = []

    @staticmethod
    def from_file(filename):
        return Intcode(read_integers(filename))

    @staticmethod
    def op_and_params(instruction):
        op = instruction % 100
        modes = []
        instruction //= 100
        while instruction > 0:
            modes.append(instruction % 10)
            instruction //= 10
        return op, modes

    def values(self, count, modes):
        """Given the memory counter and params, return COUNT values according"""
        values = []
        for i in range(count):
            if i >= len(modes) or modes[i] == 0:
                values.append(self._memory[self._memory[self.pos + i + 1]])
            elif modes[i] == 1:
                values.append(self._memory[self.pos + i + 1])
            elif modes[i] == 2:
                values.append(self._memory[self._memory[self.pos + i + 1] + self.relative_base])
            else:
                raise ValueError
        return values

    def reset(self, inp: Optional[list] = None):
        for i in range(len(self._program)):
            self._memory[i] = self._program[i]
        self._input = inp[:] if inp else []
        self.pos = 0
        self.relative_base = 0

    def run_until_output(self) -> Optional[int]:
        """Runs Intcode on a given input, producing given output."""
        while self._memory[self.pos] != Intcode.EXIT:
            op, modes = Intcode.op_and_params(self._memory[self.pos])
            if op == Intcode.ADD:
                relative = self.relative_base if len(modes) == 3 and modes[2] == 2 else 0
                x, y = self.values(2, modes)
                self._memory[self._memory[self.pos + 3] + relative] = x + y
                self.pos += 4
            elif op == Intcode.MUL:
                relative = self.relative_base if len(modes) == 3 and modes[2] == 2 else 0
                x, y = self.values(2, modes)
                self._memory[self._memory[self.pos + 3] + relative] = x * y
                self.pos += 4
            elif op == Intcode.READ:
                relative = self.relative_base if modes and modes[0] == 2 else 0
                self._memory[self._memory[self.pos + 1] + relative] = self._input.pop(0)
                self.pos += 2
            elif op == Intcode.WRITE:
                x, = self.values(1, modes)
                self.pos += 2
                return x
            elif op == Intcode.JUMP_IF_TRUE:
                x, y = self.values(2, modes)
                if x != 0:
                    self.pos = y
                else:
                    self.pos += 3
            elif op == Intcode.JUMP_IF_FALSE:
                x, y = self.values(2, modes)
                if x == 0:
                    self.pos = y
                else:
                    self.pos += 3
            elif op == Intcode.LESS:
                x, y = self.values(2, modes)
                relative = self.relative_base if len(modes) == 3 and modes[2] == 2 else 0
                self._memory[self._memory[self.pos + 3] + relative] = (1 if x < y else 0)
                self.pos += 4
            elif op == Intcode.EQUALS:
                x, y = self.values(2, modes)
                relative = self.relative_base if len(modes) == 3 and modes[2] == 2 else 0
                self._memory[self._memory[self.pos + 3] + relative] = (1 if x == y else 0)
                self.pos += 4
            elif op == Intcode.ADJUST_REL_BASE:
                x, = self.values(1, modes)
                self.relative_base += x
                self.pos += 2
            else:
                raise ValueError(f'Unexpected code {self._memory[self.pos]} at position {self.pos}.\n{self._memory=}')
        return None

    def run(self, inp: Optional[list] = None) -> list:
        self.reset(inp)
        output = []
        while (o := self.run_until_output()) is not None:
            output.append(o)
        return output

    def append_input(self, x):
        self._input.append(x)

    @property
    def memory(self):
        """Return the state of the memory after the run."""
        return self._memory
