from intcode import Intcode


EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)
SYMBOL = {EMPTY: ' ', WALL: 'W', BLOCK: '\u2592', PADDLE: '\u2582', BALL: '\u25EF'}


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


class Arcade:
    def __init__(self, filename, quarters=None):
        self.brain = Intcode.from_file(filename)
        self.brain.reset()
        if quarters is not None:
            self.brain.memory[0] = quarters
        self.screen = {}
        self.score = 0
        self.ball = -1
        self.paddle = -1
        self.brain.input_fn = lambda: sign(self.ball-self.paddle)

    def draw(self, count=962):
        for _ in range(count):
            x = self.brain.run_until_output()
            y = self.brain.run_until_output()
            tile = self.brain.run_until_output()
            if tile == PADDLE:
                self.paddle = x
            elif tile == BALL:
                self.ball = x
            if x == -1 and y == 0:
                self.score = tile
            else:
                self.screen[(x, y)] = tile

    def __str__(self):
        xcoord = [c[0] for c in self.screen.keys() if c[0] is not None]
        ycoord = [c[1] for c in self.screen.keys() if c[1] is not None]
        xmin, xmax = min(xcoord), max(xcoord)
        ymin, ymax = min(ycoord), max(ycoord)

        def symbol(x, y):
            c = self.screen.get((x, y), EMPTY)
            if c == WALL:
                if y == ymin:
                    if x == xmin:
                        return '\u250C'
                    elif x == xmax:
                        return '\u2510'
                    else:
                        return '\u2500'
                elif x == xmin or x == xmax:
                    return '\u2502'
            else:
                return SYMBOL[c]


        result = []
        for y in range(ymin, ymax+1):
            result.append(''.join(symbol(x, y) for x in range(xmin, xmax+1)))

        return '\n'.join(result) + '\n' + str(self.score)


def test_part1():
    a = Arcade('inputs/day13.txt')
    a.draw()
    assert len([x for x in a.screen if a.screen[x] == BLOCK]) == 372


def test_part2():
    a = Arcade('inputs/day13.txt', 2)
    for _ in range(30):
        a.draw()
    assert a.score == 19297


if __name__ == '__main__':
    a = Arcade('inputs/day13.txt', 2)
    for _ in range(30):
        a.draw()
        print(a)
