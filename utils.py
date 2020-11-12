def read_integers(filename):
    return [int(x) for x in open(filename).read().split(',')]

def read_digits(filename):
    return [int(x) for x in open(filename).read().strip()]
