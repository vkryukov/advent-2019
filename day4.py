def how_many_passwords():
    return sum(
        (a == b and b != c) or
        (a != b and b == c and c != d) or
        (b != c and c == d and d != e) or
        (c != d and d == e and e != f) or
        (d != e and e == f)
        for a in range(1, 10)
        for b in range(a, 10)
        for c in range(b, 10)
        for d in range(c, 10)
        for e in range(d, 10)
        for f in range(e, 10)
        if 264793 <= (100_000 * a + 10_000 * b + 1_000 * c + 100 * d + 10 * e + f) <= 803935
    )


if __name__ == '__main__':
    print(how_many_passwords())
