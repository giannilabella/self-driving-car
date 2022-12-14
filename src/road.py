import tkinter as tk

from utils import lerp
from _types import Point, Line, LineList, LineTupleCanvasIdList

class Road :
    def __init__ (self, x: float, width: float, lane_count = 3) -> None:
        self.__x = x
        self.__width = width
        self.__lane_count = lane_count

        self.__left = self.__x - width / 2
        self.__right = self.__x + width / 2

        infinity = 100_000_000
        self.__top = -infinity
        self.__bottom = infinity

        top_left = Point(self.__left, self.__top)
        top_right = Point(self.__right, self.__top)
        bottom_left = Point(self.__left, self.__bottom)
        bottom_right = Point(self.__right, self.__bottom)
        self.__borders: LineList = [
            Line(top_left, bottom_left),
            Line(top_right, bottom_right)
        ]
        
        self.__animated_line_y = 0

    @property
    def borders (self) :
        return self.__borders

    def get_lane_center (self, lane_index: int) :
        lane_index = min(lane_index, self.__lane_count - 1)
        lane_width = self.__width / self.__lane_count

        return self.__left + lane_width / 2 + lane_index * lane_width
    
    def animate_lines (self, canvas: tk.Canvas, vertical_movement: float) :
        canvas_height = canvas.winfo_height()
        
        # Check if car is approaching canvas limits
        approaching = None
        self.__animated_line_y += vertical_movement
        if self.__animated_line_y >= canvas_height / 2 :
            approaching = 'TOP'
            self.__animated_line_y -= canvas_height
        elif self.__animated_line_y <= -canvas_height / 2 :
            approaching = 'BOTTOM'
            self.__animated_line_y += canvas_height
        
        for tuple_index, lines_tuple in enumerate(self.__dashed_lines_ids) :
            # Move lines to simulate car movement
            canvas.move(lines_tuple[0], 0, vertical_movement)
            canvas.move(lines_tuple[1], 0, vertical_movement)
            canvas.move(lines_tuple[2], 0, vertical_movement)
            
            if approaching == 'TOP' :
                # Move 3rd line to top and swap positions
                canvas.move(lines_tuple[2], 0, -3 * canvas_height - vertical_movement)
                self.__dashed_lines_ids[tuple_index] = lines_tuple[2], lines_tuple[0], lines_tuple[1]

            elif approaching == 'BOTTOM' :
                # Move 1st line to bottom and swap positions
                canvas.move(lines_tuple[0], 0, 3 * canvas_height - vertical_movement)
                self.__dashed_lines_ids[tuple_index] = lines_tuple[1], lines_tuple[2], lines_tuple[0]
                

    def draw (self, canvas: tk.Canvas) :
        self.__dashed_lines_ids: LineTupleCanvasIdList = []

        for i in range(1, self.__lane_count) :
            line_x = lerp(
                self.__left, self.__right,
                i / self.__lane_count
            )

            self.__dashed_lines_ids.append((
                canvas.create_line(
                    line_x, -canvas.winfo_height(),
                    line_x, 0,
                    fill='white', width=5,
                    dash=(255, 5)
                ),
                canvas.create_line(
                    line_x, 0,
                    line_x, canvas.winfo_height(),
                    fill='white', width=5,
                    dash=(255, 5)
                ),
                canvas.create_line(
                    line_x, canvas.winfo_height(),
                    line_x, 2 * canvas.winfo_height(),
                    fill='white', width=5,
                    dash=(255, 5)
                )
            ))
            
        for border in self.__borders :
            canvas.create_line(
                border[0].x, 0,
                border[1].x, canvas.winfo_height(),
                fill='white',
                width=5
            )