from typing import Optional

from utils import read_digits


class Layer:
    def __init__(self, wide: int, tall: int, data: Optional[list] = None):
        if data is None:
            data = [None] * (wide * tall)
        self._data = [[data[t * wide + w] for w in range(wide)] for t in range(tall)]
        self.wide = wide
        self.tall = tall

    def __getitem__(self, key):
        i, j = key
        return self._data[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self._data[i][j] = value

    def count(self, x):
        return sum(line.count(x) for line in self._data)


class Image:
    def __init__(self, data: list, size: tuple):
        wide, tall = size
        layers_count = len(data) // wide // tall
        layers = []
        for i in range(layers_count):
            layer = Layer(wide, tall, data[i * wide * tall: (i + 1) * wide * tall])
            layers.append(layer)
        self.layers = layers
        self.wide = wide
        self.tall = tall

    def full_image(self):
        full = Layer(self.wide, self.tall)
        for j in range(self.wide):
            for i in range(self.tall):
                for layer in self.layers:
                    if layer[(i, j)] != 2:
                        full[(i, j)] = layer[(i, j)]
                        break
        return full

    def print(self):
        for line in self.full_image()._data:
            for ch in line:
                if ch == 0:
                    print(' ', end='')
                else:
                    print('x', end='')
            print()


def test_layer():
    l1 = Layer(3, 2, range(1, 7))
    assert l1._data[0] == [1, 2, 3]
    assert l1._data[1] == [4, 5, 6]
    assert l1[(0, 0)] == 1
    assert l1[(1, 1)] == 5
    assert l1[(0, 2)] == 3
    assert l1[(1, 2)] == 6


def test_image():
    img = Image([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], (3, 2))
    assert img.layers[0]._data[0] == [1, 2, 3]
    assert img.layers[0]._data[1] == [4, 5, 6]
    assert img.layers[1]._data[0] == [7, 8, 9]
    assert img.layers[1]._data[1] == [0, 1, 2]


def test_part1():
    img = Image(read_digits('inputs/day8.txt'), (25, 6))
    fewest = min([(x.count(0), x.count(1), x.count(2)) for x in img.layers], key=lambda x: x[0])
    assert fewest[1]*fewest[2] == 1584


def test_full_image():
    img = Image([int(x) for x in '0222112222120000'], (2,2))
    assert img.full_image()._data == [[0, 1], [1, 0]]


def test_part2():
    img = Image(read_digits('inputs/day8.txt'), (25, 6))
    img.print()


if __name__ == '__main__':
    test_part2()