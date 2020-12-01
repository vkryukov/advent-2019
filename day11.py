from intcode import Intcode

UP, DOWN, LEFT, RIGHT = (0, 1), (0, -1), (-1, 0), (1, 0)

TURN_LEFT = (UP, LEFT, DOWN, RIGHT, UP)
TURN_RIGHT = (UP, RIGHT, DOWN, LEFT, UP)


class Robot:
    def __init__(self, /, start=(0, 0), white_panels=(), black_panels=()):
        self.dir = UP
        self.x, self.y = start
        self.colors = {}
        for p in white_panels:
            self.colors[p] = 1
        for p in black_panels:
            self.colors[p] = 0

    def process(self, color, turn):
        if color == 0:
            # Paint black
            self.colors[(self.x, self.y)] = 0
        else:
            # Paint white
            self.colors[(self.x, self.y)] = 1

        if turn == 0:
            # Turn left
            self.dir = TURN_LEFT[TURN_LEFT.index(self.dir) + 1]
        else:
            # Turn right
            self.dir = TURN_RIGHT[TURN_RIGHT.index(self.dir) + 1]

        x, y = self.dir
        self.x, self.y = self.x + x, self.y + y

    def color(self, pos=None):
        x, y = pos if pos else (self.x, self.y)
        return self.colors.get((x, y), 0)

    def __str__(self):
        x_coords = [p[0] for p in self.colors.keys()]
        y_coords = [p[1] for p in self.colors.keys()]
        min_x = min(-2, min(x_coords) - 1 if x_coords else 0)
        max_x = max(2, max(x_coords) + 1 if x_coords else 0)
        min_y = min(-2, min(y_coords) - 1 if y_coords else 0)
        max_y = max(2, max(y_coords) + 1 if y_coords else 0)

        symbol = {UP: '^', LEFT: '<', RIGHT: '>', DOWN: 'v'}

        ss = []
        for r in range(max_y, min_y - 1, -1):
            s = ''
            for c in range(min_x, max_x + 1):
                if (c, r) == (self.x, self.y):
                    s += symbol[self.dir]
                elif self.color((c, r)) == 0:
                    s += '.'
                else:
                    s += '#'
            ss.append(s)
        return '\n'.join(ss)

    @property
    def painted_panels(self):
        return len(self.colors.keys())


def test_robot():
    r = Robot()
    assert str(r) == """.....
.....
..^..
.....
....."""

    r.process(1, 0)
    assert str(r) == """.....
.....
.<#..
.....
....."""

    r.process(0, 0)
    assert str(r) == """.....
.....
..#..
.v...
....."""

    r.process(1, 0)
    r.process(1, 0)
    assert str(r) == """.....
.....
..^..
.##..
....."""

    r.process(0, 1)
    r.process(1, 0)
    r.process(1, 0)
    assert str(r) == """.....
..<#.
...#.
.##..
....."""

    assert r.painted_panels == 6


class RobotWithProgram(Robot):
    def __init__(self, filename, /, white_panels=(), black_panels=()):
        self.brain = Intcode.from_file(filename)
        self.brain.reset()
        super().__init__(white_panels = white_panels, black_panels=black_panels)

    def paint(self):
        while True:
            self.brain.append_input(self.color())
            color = self.brain.run_until_output()
            if color is None:
                return
            turn = self.brain.run_until_output()
            self.process(color, turn)


def test_part1():
    r = RobotWithProgram('inputs/day11.txt')
    r.paint()
    assert r.painted_panels == 2594


def test_part2():
    r = RobotWithProgram('inputs/day11.txt', white_panels=((0, 0),))
    r.paint()
    print(r)
    assert str(r) == """..............................................
..............................................
....##..#..#.####.###....##.####.#..#.#..#....
...#..#.#.#..#....#..#....#.#....#..#.#.#.....
...#..#.##...###..#..#....#.###..####.##......
...####.#.#..#....###.....#.#....#..#.#.#.....
...#..#.#.#..#....#.#..#..#.#....#..#.#.#..>..
...#..#.#..#.####.#..#..##..#....#..#.#..#....
.............................................."""
