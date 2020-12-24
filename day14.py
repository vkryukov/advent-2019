from collections import namedtuple, defaultdict
import math

from utils import Input


class Ingredients:
    def __init__(self, lst=''):
        self.amount = {}
        for s in lst.split(', '):
            a, n = s.split()
            self.amount[n] = int(a)

    def from_ore(self):
        keys = self.amount.keys()
        return len(keys) == 1 and 'ORE' in keys

    def ore(self, needed):
        if not self.from_ore():
            raise ValueError
        return needed * self.amount['ORE']

    def components(self):
        return self.amount.keys()


Formula = namedtuple('Formula', 'amount ingredients')

TRILLION = 1_000_000_000_000


class Reactions(dict):
    def __init__(self, s):
        super().__init__()
        for line in s.splitlines():
            ingr, output = line.split(' => ')
            amount, name = output.split()
            self[name] = Formula(amount=int(amount), ingredients=Ingredients(ingr))

        self.dependants = {
            c: {name for name, f in self.items() if c in f.ingredients.components()}
            for c in self
        }

    def fuel(self, start=1):
        d = defaultdict(int)
        d['FUEL'] = start
        generated = set()

        proceed = all(self[k].ingredients.from_ore() for k in d)
        while not proceed:
            keys = list(d.keys())
            for ch in keys:
                if self.dependants[ch] - generated == set():
                    f = self[ch].ingredients
                    if f.from_ore():
                        continue
                    for name, amount in f.amount.items():
                        d[name] += math.ceil(d[ch] / self[ch].amount) * amount
                    generated.add(ch)
                    del d[ch]
            proceed = all(self[k].ingredients.from_ore() for k in d)

        return sum(math.ceil(target / self[name].amount) * self[name].ingredients.amount['ORE']
                   for name, target in d.items())

    def find_trillion(self):
        start = TRILLION // self.fuel(1)
        end = 2 * TRILLION
        while start < end:
            m = (start + end) // 2
            f = self.fuel(m)
            if f == TRILLION:
                return m
            elif f < TRILLION:
                start = m + 1
            else:
                end = m - 1
        return start - 1

def test_ingredients():
    i = Ingredients('44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ')
    assert i.amount == dict(XJWVT=44, KHKGT=5, QDVJ=1, NZVS=29, GPVTF=9, HKGWZ=48)
    assert not i.from_ore()

    i = Ingredients('157 ORE')
    assert i.amount == dict(ORE=157)
    assert i.from_ore()


def test_reactions():
    r = Reactions("""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""")
    assert r['A'].amount == 10
    assert r['A'].ingredients.from_ore()
    assert r['B'].amount == 1
    assert r['B'].ingredients.from_ore()
    assert not r['C'].ingredients.from_ore()

    assert r.dependants['A'] == {'C', 'D', 'E', 'FUEL'}
    assert r.dependants['B'] == {'C'}
    assert r.dependants['C'] == {'D'}
    assert r.dependants['D'] == {'E'}
    assert r.dependants['E'] == {'FUEL'}


def test_fuel():
    for s, answer, trillion in (
        ("""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""", 31, 0),
        ("""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""", 165, 0),
        ("""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""", 13312, 82892753),
        ("""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""", 180697, 5586022),
        ("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""", 2210736, 460664),
    ):
        r = Reactions(s)
        assert r.fuel() == answer
        if trillion != 0:
            assert r.fuel(trillion) <= 1_000_000_000_000
            assert r.fuel(trillion + 1) > 1_000_000_000_000
            assert r.find_trillion() == trillion


def test_part1():
    assert Reactions(Input(14, year=2019)).fuel() == 532506


def test_part2():
    assert Reactions(Input(14, year=2019)).find_trillion() == 2595245
