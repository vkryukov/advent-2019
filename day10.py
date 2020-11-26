import math
import typing
from collections import namedtuple, defaultdict

ACCURATE_DIGITS = 4
ACCURACY = math.pow(0.1, ACCURATE_DIGITS)


class Point(namedtuple('Point', 'x y')):
    """A point on two-dimensional grid."""

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __eq__(self, other: 'Point') -> bool:
        """Equality with a given ACCURACY"""
        return abs(self.x - other.x) < ACCURACY and abs(self.y - other.y) < ACCURACY

    def __hash__(self):
        return hash((round(self.x, ACCURATE_DIGITS), round(self.y, ACCURATE_DIGITS)))

    def __le__(self, other) -> bool:
        p1, p2 = self.norm(), other.norm()
        if p1 == p2:
            return abs(self) <= abs(other)
        if p1.x >= 0 and p2.x < 0:
            return True
        elif p1.x < 0 and p2.x >= 0:
            return False
        elif p1.x >= 0 and p2.x >= 0:
            return p1.y <= p2.y
        else:
            return p1.y >= p2.y

    def __lt__(self, other):
        return self <= other and self != other

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


def test_point_comparison():
    points = [
        (0, -1), (0, -2), (0, -3),
        (1, -3), (1, -2), (2, -3),
        (1, -1), (2, -2), (3, -3),
        (3, -2), (2, -1), (3, -1),
        (1, 0), (2, 0), (3, 0),
        (3, 1),
        (1, 1), (2, 2),
        (2, 3),
        (0, 1),
        (0, 3),
        (-1, 3),
        (-1, 1),
        (-2, 2),
        (-3, 1),
        (-1, 0), (-2, 0), (-3, 0),
        (-3, -1), (-2, -1),
        (-1, -1), (-2, -2),
        (-2, -3),
        (-1, -3),
    ]
    for i in range(len(points) - 1):
        x, y = points[i]
        x1, y1 = points[i + 1]
        assert Point(x, y) < Point(x1, y1)


def group_by(lst: typing.Iterable, /, key, sort_key=None) -> dict:
    """Groups LST elements by the value of KEY, and returns a dictionary mapping the value of key
    to all elements of LST with the given key. SORT_KEY, if set, sorts each of these lists."""
    d = defaultdict(list)
    for el in lst:
        d[key(el)].append(el)
    if sort_key:
        for el in d:
            d[el] = sorted(d[el], key=sort_key)
    return dict(d)


def test_group_by():
    lst = range(10)
    assert group_by(lst, key=lambda x: x % 2) == {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
    assert group_by(['mother', 'window', 'Mary', 'wash'], key=lambda s: s[0].lower()) == dict(
        m=['mother', 'Mary'],
        w=['window', 'wash']
    )
    assert group_by(['mother', 'wash', 'Mary', 'window'],
                    key=lambda s: s[0].lower(),
                    sort_key=len
                    ) == dict(
        m=['Mary', 'mother'],
        w=['wash', 'window']
    )


class Map:
    """A two-dimensional collection of points."""

    def __init__(self, w: int, h: int, points: list[Point]):
        self.w, self.h = w, h
        self.points = points
        self.monitoring = None
        self.vaporization_order = None

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

    def set_station(self, x, y):
        """Set a monitoring station at point (x, y)."""
        p = Point(x, y)
        assert p in self.points
        self.monitoring = p
        self.mark_vaporization()

    def mark_vaporization(self):
        """Mark everything that's going to be vaporized after the first rotation"""
        other_points = [p for p in self.points if p != self.monitoring]
        groups = group_by(other_points,
                          key=lambda p: self.monitoring.direction(p).norm(),
                          sort_key=lambda p: self.monitoring.direction(p))
        for key in groups:
            for i in range(len(groups[key])):
                groups[key][i].order = i + 1
        self.vaporization_order = sorted(other_points, key=lambda p: (p.order, self.monitoring.direction(p)))


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


def test_mark_first_9_vaporized():
    m = Map.from_str(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""")
    m.set_station(8, 3)

    def mark(m, p):
        if p == m.monitoring:
            return 'X'
        else:
            idx = m.vaporization_order.index(p)
            if idx < 9:
                return str(idx + 1)
            else:
                return '#'

    assert m.display(lambda p: mark(m, p)) == """.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##"""


def test_vaporization():
    m = Map.from_str(""".#..##.###...#######
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
###.##.####.##.#..##""")
    m.set_station(11, 13)
    vapor = m.vaporization_order
    for i, x, y in [
        (1, 11, 12),
        (2, 12, 1),
        (3, 12, 2),
        (10, 12, 8),
        (20, 16, 0),
        (50, 16, 9),
        (100, 10, 16),
        (199, 9, 6),
        (200, 8, 2),
        (201, 10, 9),
        (299, 11, 1)
    ]:
        assert vapor[i - 1] == Point(x, y)
    assert len(vapor) == 299


def test_part1():
    assert Map.from_str(open('inputs/day10.txt').read()).best_observability()[2] == 278


def test_part2():
    m = Map.from_str(open('inputs/day10.txt').read())
    x, y, most = m.best_observability()
    assert most == 278
    m.set_station(x, y)
    assert m.vaporization_order[199] == Point(14, 17)
