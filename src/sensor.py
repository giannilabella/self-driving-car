import numpy as np
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING :
    from car import Car
from utils import lerp, get_intersection
from _types import (
    Point, Line, Reading,
    LineList, ReadingList, CanvasIdList
)

class Sensor :
    def __init__ (self, car: 'Car') -> None:
        self.__car = car
        self.__ray_count = 5
        self.__ray_length = 150
        self.__ray_spread = np.pi / 2

        self.__rays: LineList = []
        self.__rays_ids: CanvasIdList = []

        self.__readings: ReadingList = []

    def __cast_rays (self) :
        self.__rays = []

        for i in range(self.__ray_count) :
            ray_angle = lerp(
                self.__ray_spread / 2,
                -self.__ray_spread / 2,
                i / (self.__ray_count - 1) if self.__ray_count != 1 else 0.5
            ) + self.__car.angle

            start = Point(self.__car.x, self.__car.y)
            end = Point(
                self.__car.x - self.__ray_length * np.sin(ray_angle),
                self.__car.y - self.__ray_length * np.cos(ray_angle)
            )

            self.__rays.append(Line(start, end))

    def __get_single_reading (self, ray: Line, road_borders: LineList) -> Reading | None :
        touches = []

        for border in road_borders :
            touch = get_intersection(
                ray.start,
                ray.end,
                border.start,
                border.end
            )
            if touch :
                touches.append(touch)

        if len(touches) == 0 :
            return None
        else :
            offsets = [touch.offset for touch in touches]
            min_offset = min(offsets)
            return [touch for touch in touches if touch.offset == min_offset][0]

    def __get_readings (self, road_borders: LineList) :
        self.__readings = []

        for ray in self.__rays :
            self.__readings.append(
                self.__get_single_reading(
                    ray, road_borders
                )
            )

    def update (self, road_borders: LineList) :
        self.__cast_rays()

        self.__get_readings(road_borders)

    def draw (self, canvas: tk.Canvas, car_fixed_y: float | None = None) :
        # Erase previous rays
        for ray_id in self.__rays_ids :
            canvas.delete(ray_id)

        self.__rays_ids = []

        # Calculate y position for drawing
        y_offset = 0
        if car_fixed_y is not None :
            y_offset = car_fixed_y - self.__car.y

        # Draw Rays
        for ray, reading in zip(self.__rays, self.__readings) :
            ray_end = ray.end
            if reading :
                ray_end = reading.point

            self.__rays_ids.extend([
                canvas.create_line(
                    ray.end.x, ray.end.y + y_offset,
                    ray_end.x, ray_end.y + y_offset,
                    fill = 'black',
                    width = 2
                ),
                canvas.create_line(
                    ray.start.x, ray.start.y + y_offset,
                    ray_end.x, ray_end.y + y_offset,
                    fill = 'yellow',
                    width = 2
                )
            ])
