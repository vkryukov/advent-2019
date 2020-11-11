def fuel_required(mass):
    return mass // 3 - 2


def test_fuel_required():
    for mass, fuel in [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583)
    ]:
        assert fuel_required(mass) == fuel


def solve(fn):
    mass = 0
    for line in open('inputs/day1.txt').readlines():
        mass += fn(int(line))
    print(f"{mass=}")


def total_mass_required(mass):
    fuel = fuel_required(mass)
    if fuel <= 0:
        return 0
    else:
        return fuel + total_mass_required(fuel)


def test_full_fuel_required():
    for mass, fuel in [
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ]:
        assert total_mass_required(mass) == fuel


if __name__ == '__main__':
    solve(total_mass_required)
