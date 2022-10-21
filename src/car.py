import numpy as np
import tkinter as tk

from controls import Controls

class Car :
    def __init__ (self, window: tk.Tk, x: float, y: float, width: float, height: float, color: str) -> None:
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        
        self.__car_item_id: tk._CanvasItemId | None = None
        self.__controls = Controls(window)

        self.__speed = 0
        self.__acceleration = 0.25
        self.__max_speed = 5
        self.__max_reverse_speed = - self.__max_speed / 2
        self.__friction = 0.05

        self.__angle = 0
        self.__steering_angle = 0.03

    @property
    def x (self) :
        return self.__x

    @property
    def y (self) :
        return self.__y

    def __move (self) -> tuple[float, float]:
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

    def update (self) -> tuple[float, float] :
        car_movement = self.__move()

        return car_movement
        
    def draw (self, canvas: tk.Canvas, car_fixed_y: float | None = None) :
        # Calculate temporary constants
        half_width = self.__width / 2
        half_height = self.__height / 2
        sin = np.sin(self.__angle)
        cos = np.cos(self.__angle)
        
        if car_fixed_y is None :
            car_y = self.__y
        else :
            car_y = car_fixed_y

        # Calculate Car corners
        top_left = [
            self.__x - half_width*cos - half_height*sin,
            car_y - half_height*cos + half_width*sin,
        ]
        top_right = [
            self.__x + half_width*cos - half_height*sin,
            car_y - half_height*cos - half_width*sin,
        ]
        bottom_right = [
            self.__x + half_width*cos + half_height*sin,
            car_y + half_height*cos - half_width*sin,
        ]
        bottom_left = [
            self.__x - half_width*cos + half_height*sin,
            car_y + half_height*cos + half_width*sin,
        ]
        
        # Erase Previous Car Position
        if self.__car_item_id is not None :
            canvas.delete(self.__car_item_id)

        # Draw Car Polygon
        self.__car_item_id = canvas.create_polygon(
            *top_left,
            *top_right,
            *bottom_right,
            *bottom_left,
            fill=self.__color, outline=self.__color
        )