class Layer:
    def __init__(self, data: list, wide: int, tall: int):
        self._data = [[data[t * wide + w] for w in range(wide)] for t in range(tall)]
        self.wide = wide
        self.tall = tall

    def __getitem__(self, key):
        i, j = key
        return self._data[i][j]


class Image:
    def __init__(self, data: list, size: tuple):
        wide, tall = size
        layers_count = len(data) // wide // tall
        layers = []
        for i in range(layers_count):
            layer = Layer(data[i * wide * tall: (i + 1) * wide * tall], wide, tall)
            layers.append(layer)
        self.layers = layers
        self.wide = wide
        self.tall = tall


def test_layer():
    l1 = Layer(range(1, 7), 3, 2)
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
