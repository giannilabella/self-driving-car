from collections import namedtuple
Point = namedtuple('Point', 'x y')

def lerp (A, B, t) :
    return A + (B - A) * t