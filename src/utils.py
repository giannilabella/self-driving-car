import numpy as np
import numpy.typing as npt

from _types import Point, Reading

def lerp (A: float, B: float, t: float) -> float :
    return A + (B - A) * t

def get_intersection (A: Point, B: Point, C: Point, D: Point) -> Reading | None :
    a = np.array([A], np.float64)
    b = np.array([B], np.float64)
    c = np.array([C], np.float64)
    d = np.array([D], np.float64)

    ab = b - a
    ac = c - a
    cd = d - c
    
    ab_cross_cd = np.cross(ab, cd)
    
    # ABxCD = 0 if they're parallel
    if ab_cross_cd == 0 :
        return None

    ac_cross_cd = np.cross(ac, cd)
    ac_cross_ab = np.cross(ac, ab)

    t1 = float(ac_cross_cd / ab_cross_cd)
    t2 = float(ac_cross_ab / ab_cross_cd)

    # Check if intersection is between segments AB and CD
    if not 0 <= t1 <= 1 or not 0 <= t2 <= 1 :
        return None

    I = Point(
        lerp(A.x, B.x, t1),
        lerp(A.y, B.y, t1)
    )
    return Reading(I, t1)

def polys_intersect (poly_1: list[Point], poly_2: list[Point]) -> bool :
    for index_1, point_1 in enumerate(poly_1) :
        for index_2, point_2 in enumerate(poly_2) :
            touch = get_intersection(
                point_1,
                poly_1[(index_1 + 1) % len(poly_1)],
                point_2,
                poly_2[(index_2 + 1) % len(poly_2)]
            )
            if touch is not None : return True
    return False

def sigmoid (x: npt.NDArray[np.float64], gain = 1) :
    return (1 / (1 + np.exp(-gain * x))).astype(np.float64)

def get_hex_color (value: float) -> str :
    # Positive: yellow, Negative: blue
    color = (255, 255, 0) if value >= 0 else (0, 0, 255)
    alpha = abs(value)

    return rgba_to_hex(*color, alpha)

def rgba_to_hex (red: int, green: int, blue: int, alpha: float = 1) -> str :
    red = int(red * alpha)
    green = int(green * alpha)
    blue = int(blue * alpha)

    return f'#{red:02x}{green:02x}{blue:02x}'