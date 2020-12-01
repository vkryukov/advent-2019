import re
import math

from utils import *

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


class Moon:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = 0, 0, 0

    def apply_gravity(self, other: 'Moon') -> None:
        self.vx += sign(other.x - self.x)
        self.vy += sign(other.y - self.y)
        self.vz += sign(other.z - self.z)

    def apply_velocity(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def __str__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>"

    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))

    def copy(self):
        return Moon(self.x, self.y, self.z)


class MoonSystem:
    def __init__(self, moons):
        self.moons = []
        for x, y, z in moons:
            self.moons.append(Moon(x, y, z))

    def step(self):
        for m1, m2 in combinations(self.moons, 2):
            m1.apply_gravity(m2)
            m2.apply_gravity(m1)
        for m in self.moons:
            m.apply_velocity()

    def steps(self, n):
        for _ in range(n):
            self.step()

    def __str__(self):
        return '\n'.join(str(m) for m in self.moons)

    def energy(self):
        return sum(m.energy() for m in self.moons)

    def print_x(self, steps):
        for _ in range(steps):
            for m in self.moons:
                print(f'({m.x}, {m.vx})', end=' ')
            print()
            self.step()

    def period(self) -> int:
        m1, m2, m3, m4 = self.moons
        o1, o2, o3, o4 = m1.copy(), m2.copy(), m3.copy(), m4.copy()
        period_x = period_y = period_z = None
        steps = 0
        while period_x is None or period_y is None or period_z is None:
            self.step()
            steps += 1
            m1, m2, m3, m4 = self.moons
            if period_x is None and m1.x == o1.x and m1.vx == o1.vx and m2.x == m2.x and m2.vx == o2.vx \
                and m3.x == o3.x and m3.vx == o3.vx:
                period_x = steps
            if period_y is None and m1.y == o1.y and m1.vy == o1.vy and m2.y == m2.y and m2.vy == o2.vy \
                    and m3.y == o3.y and m3.vy == o3.vy:
                period_y = steps
            if period_z is None and m1.z == o1.z and m1.vz == o1.vz and m2.z == m2.z and m2.vz == o2.vz \
                    and m3.z == o3.z and m3.vz == o3.vz:
                period_z = steps

        return math.lcm(period_x, period_y,period_z)


def clean(s): return re.sub('=\s*', '=', s)


def test_moon_system():
    ms = MoonSystem((
        (-1, 0, 2),
        (2, -10, -7),
        (4, -8, 8),
        (3, 5, -1)))

    assert str(ms) == clean("""pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>""")

    ms.step()
    assert str(ms) == clean("""pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>""")

    ms.step()
    assert str(ms) == clean("""pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>""")

    ms.steps(3)
    assert str(ms) == clean("""pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>""")

    ms.steps(5)
    assert str(ms) == clean("""pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>""")
    assert ms.energy() == 179




def test_moon_system2():
    ms = MoonSystem((
        (-8, -10, 0),
        (5, 5, 10),
        (2, -7, 3),
        (9, -8, -3)
    ))
    assert str(ms) == clean("""pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>""")

    ms.steps(50)
    assert str(ms) == clean("""pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>""")

    ms.steps(50)
    assert str(ms) == clean("""pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>""")
    assert ms.energy() == 1940


def test_part1():
    ms = MoonSystem((
        (-13, -13, -13),
        (5, -8, 3),
        (-6, -10, -3),
        (0, 5, -5),
    ))
    ms.steps(1000)
    assert ms.energy() == 8044


def test_periods():
    ms = MoonSystem((
        (-1, 0, 2),
        (2, -10, -7),
        (4, -8, 8),
        (3, 5, -1)))
    assert ms.period() == 2772

    ms = MoonSystem((
        (-8, -10, 0),
        (5, 5, 10),
        (2, -7, 3),
        (9, -8, -3)
    ))
    assert ms.period() == 4686774924


def test_part2():
    ms = MoonSystem((
        (-13, -13, -13),
        (5, -8, 3),
        (-6, -10, -3),
        (0, 5, -5),
    ))
    assert ms.period() == 362375881472136
