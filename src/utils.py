import numpy as np

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
    cd = d - C
    
    ab_cross_cd = np.cross(ab, cd)
    
    # ABxCD = 0 if they're parallel
    if ab_cross_cd == 0 :
        return None

    ac_cross_cd = np.cross(ac, cd)
    ac_cross_ab = np.cross(ac, ab)

    t1 = float(ac_cross_cd / ab_cross_cd)
    t2 = float(ac_cross_ab / ab_cross_cd)

    # Check if intersection is in line segments AB and CD
    if not 0 <= t1 <= 1 or not 0 <= t2 <= 1 :
        return None

    I = Point(
        lerp(A.x, B.x, t1),
        lerp(A.y, B.y, t1)
    )
    return Reading(I, t1)