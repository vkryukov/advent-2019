def parse_map(m):
    d = {}
    for line in m.split():
        if line != "":
            large, small = line.split(')')
            d[small] = large
    return d

MAP1 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""


def calculate_weights(m):
    d = parse_map(m)
    weights = {'COM': 0}
    for _ in range(len(d) - 1):
        for small, large in d.items():
            w = weights.get(large)
            if w is not None:
                weights[small] = w + 1
    return sum(v for v in weights.values())


def test_calculate_weights():
    assert calculate_weights(MAP1) == 42


def test_part1():
    assert calculate_weights(open('inputs/day6.txt').read()) == 145250


def orbital_transfers(m):
    d = parse_map(m)

    def steps_from(planet):
        nonlocal d
        planet = d[planet]
        current_step = 0
        steps = {planet: current_step}
        while planet != 'COM':
            planet = d[planet]
            current_step += 1
            steps |= {planet: current_step}
        return steps

    you = steps_from('YOU')
    santa = steps_from('SAN')

    overlap = set(you.keys()).intersection(santa.keys())
    return min(you[k] for k in overlap) + min(santa[k] for k in overlap)


def test_orbital_transfer():
    m = """
    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN
    """
    assert orbital_transfers(m) == 4


def test_part2():
    assert orbital_transfers(open('inputs/day6.txt').read()) == 274
