import tkinter as tk

from utils import Point, lerp

class Road :
    def __init__ (self, x: float, width: float, lane_count = 3) -> None:
        self.__x = x
        self.__width = width
        self.__lane_count = lane_count

        self.__left = self.__x - width / 2
        self.__right = self.__x + width / 2

        infinity = 10000000
        self.__top = - infinity
        self.__bottom = infinity

        top_left = Point(self.__left, self.__top)
        top_right = Point(self.__right, self.__top)
        bottom_left = Point(self.__left, self.__bottom)
        bottom_right = Point(self.__right, self.__bottom)
        self.__borders = [
            [top_left, bottom_left],
            [top_right, bottom_right]
        ]

    @property
    def borders (self) :
        return self.__borders

    def get_lane_center (self, lane_index: int) :
        lane_index = min(lane_index, self.__lane_count - 1)
        lane_width = self.__width / self.__lane_count

        return self.__left + lane_width / 2 + lane_index * lane_width

    def y_translate (self, canvas: tk.Canvas, y: float) :
        for line_id in self.__line_ids :
            canvas.move(line_id, 0, y)

    def draw (self, canvas: tk.Canvas) :
        self.__line_ids: list[tk._CanvasItemId] = []

        for i in range(1, self.__lane_count) :
            line_x = lerp(self.__left, self.__right, i / self.__lane_count)

            self.__line_ids.append(
                canvas.create_line(
                    line_x, self.__top,
                    line_x, self.__bottom,
                    fill='white', width=5,
                    dash=(255, 5) # dash - 25 / gap - 5
                )
            )

        for border in self.__borders :
            self.__line_ids.append(
                canvas.create_line(
                    border[0],
                    border[1],
                    fill='white',
                    width=5
                )
            )