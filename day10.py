import math
from collections import namedtuple

ACCURATE_DIGITS = 4
ACCURACY = math.pow(0.1, ACCURATE_DIGITS)


class Point(namedtuple('Point', 'x y')):
    """A point on two-dimensional grid."""
    def __abs__(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def __eq__(self, other: 'Point') -> bool:
        """Equality with a given ACCURACY"""
        return abs(self.x - other.x) < ACCURACY and abs(self.y - other.y) < ACCURACY

    def __hash__(self):
        return hash((round(self.x, ACCURATE_DIGITS), round(self.y, ACCURATE_DIGITS)))

    def norm(self) -> 'Point':
        """Return normalized version of self."""
        a = abs(self)
        if a > 0:
            return Point(self.x / a, self.y / a)
        else:
            return Point(0, 0)

    def direction(self, other: 'Point') -> 'Point':
        """Return a direction vector from self to other."""
        return Point(other.x - self.x, other.y - self.y)

    def observable(self, points: list['Point']):
        """Return number of points observable from the current one (ignoring itself)."""
        return len({self.direction(p).norm() for p in points if self != p})


def test_point_equality():
    assert Point(1, 2) in [Point(0, 0), Point(1, 2), Point(3, 4)]
    assert Point(1.0, 2.0) == Point(1, 2)
    assert Point(1.0000001, 1.9999999) == Point(1, 2)
    assert len({Point(1, 2), Point(1.0000001, 1.9999999)}) == 1


class Map:
    """A two-dimensional collection of points."""
    def __init__(self, w: int, h: int, points: list[Point]):
        self.w = w
        self.h = h
        self.points = points

    @staticmethod
    def from_str(s: str) -> 'Map':
        """Generate a map from a string representation."""
        s = s.split()
        w, h = len(s[0]), len(s)
        points = []
        for y in range(h):
            for x in range(w):
                if s[y][x] == '#':
                    points.append(Point(x, y))
        return Map(w, h, points)

    def __str__(self):
        return self.display(lambda p: '#')

    def display(self, fn) -> str:
        """The opposite of from_str."""
        s = [['.' for _ in range(self.w)] for _ in range(self.h)]
        for p in self.points:
            s[p.y][p.x] = fn(p)
        return '\n'.join(''.join(line) for line in s)

    def print_observability(self) -> str:
        return self.display(lambda p: str(p.observable(self.points)))

    def best_observability(self) -> (int, int, int):
        best = max(self.points, key=lambda p: p.observable(self.points))
        return best.x, best.y, best.observable(self.points)


def test_map_from_str():
    s = """.#..##
.....#
#####.
....#.
...###"""
    m = Map.from_str(s)
    assert str(m) == s
    assert m.w == 6
    assert m.h == 5
    assert Point(3, 4) in m.points
    assert Point(1, 0) in m.points
    assert Point(0, 1) not in m.points


def test_observability():
    assert Map.from_str(""".#..#
.....
#####
....#
...##""").print_observability() == """.7..7
.....
67775
....7
...87"""


def test_best_observability():
    assert Map.from_str("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""").best_observability() == (5, 8, 33)
    assert Map.from_str("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""").best_observability() == (1, 2, 35)
    assert Map.from_str(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""").best_observability() == (6, 3, 41)
    assert Map.from_str(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""").best_observability() == (11, 13, 210)


def test_part1():
    assert Map.from_str(open('inputs/day10.txt').read()).best_observability()[2] == 278
