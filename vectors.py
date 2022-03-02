import math


def parse_values(func):
    def _func(self, arg):
        if isinstance(arg, Vector):
            assert len(arg) == len(self), "Vectors must have matching sizes"
            return func(self, arg._data)
        else:
            return func(self, [arg] * len(self))

    return _func


def property_for(idx):
    def _get(self):
        return self._data[idx]

    def _set(self, val):
        self._data[idx] = val

    return property(_get, _set)


class Vector:
    def __init__(self, *data):
        self._data = list(data)

    def __repr__(self):
        return repr(tuple(self._data))

    def __len__(self):
        return len(self._data)

    def __neg__(self):
        return Vector(*[-a for a in self._data])

    def size(self):
        total = sum([a**2 for a in self._data])
        return math.sqrt(total)

    def distance(self, vec):
        return (self - vec).size()

    @parse_values
    def __add__(self, arg):
        return Vector(*[self._data[i] + arg[i] for i in range(len(arg))])

    @parse_values
    def __sub__(self, arg):
        return Vector(*[self._data[i] - arg[i] for i in range(len(arg))])

    @parse_values
    def __mul__(self, arg):
        return Vector(*[self._data[i] * arg[i] for i in range(len(arg))])

    @parse_values
    def __truediv__(self, arg):
        return Vector(*[self._data[i] / arg[i] for i in range(len(arg))])

    @parse_values
    def __mod__(self, arg):
        return Vector(*[self._data[i] % arg[i] for i in range(len(arg))])

    x = property_for(0)
    y = property_for(1)
    z = property_for(2)

    a = property_for(0)
    b = property_for(1)
    c = property_for(2)

    w = property_for(0)
    h = property_for(1)
    l = property_for(2)

    width = property_for(0)
    height = property_for(1)
    length = property_for(2)

    lat = property_for(0)
    long = property_for(1)
    alt = property_for(2)

    pitch = property_for(0)
    roll = property_for(1)
    yaw = property_for(2)
