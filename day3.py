from collections import namedtuple
from typing import Optional

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


class Point(namedtuple('Point', 'x y')):
    __slots__ = ()

    def move(self, dir) -> 'Point':
        x, y = DIRECTIONS[dir[0]]
        n = int(dir[1:])
        x *= n
        y *= n
        return Point(self.x + x, self.y + y)

    @staticmethod
    def moves(dirs):
        current = Point(0, 0)
        moves = [current]
        for d in dirs.split(','):
            current = current.move(d)
            moves.append(current)
        return moves

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)


def test_point():
    assert Point(0, 0).move('R8').move('U5').move('L5').move('D3') == Point(3, 2)
    assert Point(0, 0).move('U7').move('R6').move('D4').move('L4') == Point(2, 3)

    assert Point.moves('R8,U5,L5,D3')[-1] == Point(3, 2)
    assert Point.moves('U7,R6,D4,L4')[-1] == Point(2, 3)


def intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Point]:
    """Return an intersection point of (p1, p2) and (p3, p4), or None if they don't intersect.

    We assume that both (p1, p2) and (p3, p4) are either horizontal or vertical."""
    assert p1.x == p2.x or p1.y == p2.y
    assert p3.x == p4.x or p3.y == p4.y

    if p1.x > p2.x or p1.y > p2.y:
        p1, p2 = p2, p1
    if p3.x > p4.x or p3.y > p4.y:
        p3, p4 = p4, p3

    if p1.x == p2.x:  # First is vertical
        if p3.x == p4.x:  # Second is also vertical
            return None
        else:
            # p1.y < p2.y and p3.x < p4.x
            if (p3.x <= p1.x <= p4.x) and (p1.y <= p3.y <= p2.y):
                return Point(p1.x, p3.y)
            else:
                return None
    else:  # First is horizontal
        if p3.y == p4.y:  # Second is also horizontal
            return None
        else:
            # p1.x < p2.x and p3.y < p4.y
            if (p1.x <= p3.x <= p2.x) and (p3.y <= p1.y <= p4.y):
                return Point(p3.x, p1.y)
            else:
                return None


def test_intersection():
    for p1, p2, p3, p4, result in (
        (Point(2,0), Point(8,0), Point(5,5), Point(5,-5), Point(5,0)),
    ):
        assert intersection(p1, p2, p3, p4) == result
        assert intersection(p2, p1, p3, p4) == result
        assert intersection(p1, p2, p4, p3) == result
        assert intersection(p2, p1, p4, p3) == result
        assert intersection(p3, p4, p1, p2) == result


def intersection_distance(wire1: str, wire2: str) -> int:
    moves1 = Point.moves(wire1)
    moves2 = Point.moves(wire2)
    intersections = []
    for i in range(len(moves1) - 1):
        for j in range(len(moves2) -1):
            x = intersection(moves1[i], moves1[i+1], moves2[j], moves2[j+1])
            if x is not None:
                intersections.append(x)

    return min(x.manhattan for x in intersections if x.manhattan != 0)


def test_intersection_distance():
    for wire1, wire2, distance in (
        ('R8,U5,L5,D3', 'U7,R6,D4,L4', 6),
        ('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83', 159),
        ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 135)
    ):
        assert intersection_distance(wire1, wire2) == distance


def main():
    lines = open('day3.txt').readlines()
    print(intersection_distance(lines[0], lines[1]))


if __name__ == '__main__':
    main()


