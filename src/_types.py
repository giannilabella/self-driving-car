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

class ControlOutput (NamedTuple) :
    forward: bool
    left: bool
    right: bool
    reverse: bool

LineList = list[Line]
ReadingList = list[Reading | None]
CanvasIdList = list[int]
LineTupleCanvasIdList = list[tuple[int, int, int]]

from typing import Literal
ControlType = Literal['KEYS', 'DUMMY', 'AI']