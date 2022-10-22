import numpy as np
import tkinter as tk

from sensor import Sensor
from controls import Controls
from utils import polys_intersect
from _types import Point, LineList

class Car :
    def __init__ (self, window: tk.Tk, x: float, y: float, width: float, height: float, color: str) -> None:
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color

        # Car Mechanics Parameters
        self.__speed = 0
        self.__acceleration = 0.25
        self.__max_speed = 5
        self.__max_reverse_speed = - self.__max_speed / 2
        self.__friction = 0.05
        self.__angle = 0
        self.__steering_angle = 0.03
        self.__damaged = False

        self.__car_id: int | None = None
        self.__sensor = Sensor(self)
        self.__controls = Controls(window)

    @property
    def x (self) :
        return self.__x

    @property
    def y (self) :
        return self.__y

    @property
    def angle (self) :
        return self.__angle

    def __move (self) -> tuple[float, float] :
        # Acceleration car
        if self.__controls.forward :
            self.__speed += self.__acceleration
        if self.__controls.reverse :
            self.__speed -= self.__acceleration
        
        # Speed limiter
        if self.__speed > self.__max_speed :
            self.__speed = self.__max_speed
        if self.__speed < self.__max_reverse_speed :
            self.__speed = self.__max_reverse_speed

        # Car friction
        if self.__speed > 0 :
            self.__speed -= self.__friction
        if self.__speed < 0 :
            self.__speed += self.__friction
        if abs(self.__speed) < self.__friction :
            self.__speed = 0

        # Steer car
        if self.__speed != 0 :
            flip = 1 if self.__speed > 0 else -1

            if self.__controls.left :
                self.__angle += self.__steering_angle * flip
            if self.__controls.right :
                self.__angle -= self.__steering_angle * flip

        # Move car
        x_movement = np.sin(self.__angle) * self.__speed
        y_movement = np.cos(self.__angle) * self.__speed
        self.__x -= x_movement
        self.__y -= y_movement

        return x_movement, y_movement
    
    def __assess_damage (self, road_borders: LineList) -> bool :
        for border in road_borders :
            if polys_intersect(
                self.__polygon,
                [*border]
            ) : return True
            
        return False

    def update (self, road_borders: LineList) -> tuple[float, float] :
        # Update Car
        car_movement = (0, 0)
        if not self.__damaged :
            car_movement = self.__move()
            self.__polygon = self.__create_polygon()
            self.__damaged = self.__assess_damage(road_borders)

        #Update Sensor
        self.__sensor.update(road_borders)

        return car_movement
    
    def __create_polygon (self,
        fixed_x: float | None = None,
        fixed_y: float | None = None
    ) :
        # Calculate temporary constants
        half_width = self.__width / 2
        half_height = self.__height / 2
        sin = np.sin(self.__angle)
        cos = np.cos(self.__angle)
        car_x = fixed_x if fixed_x else self.__x
        car_y = fixed_y if fixed_y else self.__y
        
        # Calculate Car corners
        return [
            Point( # Top Left
                car_x - half_width*cos - half_height*sin,
                car_y - half_height*cos + half_width*sin,
            ),
            Point( # Top Right
                car_x + half_width*cos - half_height*sin,
                car_y - half_height*cos - half_width*sin,
            ),
            Point( # Bottom Right
                car_x + half_width*cos + half_height*sin,
                car_y + half_height*cos - half_width*sin,
            ),
            Point( # Bottom Left
                car_x - half_width*cos + half_height*sin,
                car_y + half_height*cos + half_width*sin,
            ),
        ]
        
    def draw (self,
        canvas: tk.Canvas,
        fixed_x: float | None = None,
        fixed_y: float | None = None
    ) :
        # Get Car corners
        corners = self.__create_polygon(fixed_x, fixed_y)
        
        # Erase Previous Car Position
        if self.__car_id is not None :
            canvas.delete(self.__car_id)

        # Draw Car Polygon
        car_color = self.__color if not self.__damaged else 'black'
        self.__car_id = canvas.create_polygon(
            *corners,
            outline = car_color,
            fill = car_color
        )

        # Draw Sensor
        self.__sensor.draw(canvas, fixed_x, fixed_y)