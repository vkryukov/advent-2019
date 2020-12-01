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
        self.coords = [x, y, z]
        self.speed = [0, 0, 0]

    def apply_gravity(self, other: 'Moon') -> None:
        for i in range(len(self.coords)):
            self.speed[i] += sign(other.coords[i] - self.coords[i])

    def apply_velocity(self) -> None:
        for i in range(len(self.coords)):
            self.coords[i] += self.speed[i]

    def __str__(self):
        x, y, z = self.coords
        vx, vy, vz = self.speed
        return f"pos=<x={x}, y={y}, z={z}>, vel=<x={vx}, y={vy}, z={vz}>"

    def energy(self):
        return sum(abs(x) for x in self.coords) * sum(abs(s) for s in self.speed)

    def copy(self):
        return Moon(*self.coords)


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

    def period(self) -> int:
        original_moons = [m.copy() for m in self.moons]
        periods = [None, None, None]
        steps = 0
        while any(x is None for x in periods):
            self.step()
            steps += 1
            for p in range(len(periods)):
                if periods[p] is None and \
                        all(self.moons[i].coords[p] == original_moons[i].coords[p] for i in range(len(self.moons))) and \
                        all(self.moons[i].speed[p] == original_moons[i].speed[p] for i in range(len(self.moons))):
                    periods[p] = steps
        return math.lcm(*periods)


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
