# Named tuples
from typing import NamedTuple

class Point (NamedTuple) :
    x: float
    y: float

class Line (NamedTuple) :
    start: Point
    end: Point

class Reading (NamedTuple) :
    point: Point
    offset: float

# List types
LineList = list[Line]
ReadingList = list[Reading | None]
CanvasIdList = list[int]
LineTupleCanvasIdList = list[tuple[int, int]]