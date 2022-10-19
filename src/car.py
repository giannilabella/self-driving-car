import numpy as np
from tkinter import Tk, Canvas

from controls import Controls

class Car :
    def __init__ (self, x, y, width, height, color: str, window: Tk) -> None:
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        
        self.__controls = Controls(window)
        
    def draw (self, canvas: Canvas) :
        half_width = self.__width / 2
        half_height = self.__height / 2
        
        canvas.create_rectangle(
            self.__x - half_width, self.__y - half_height,
            self.__x + half_width, self.__y + half_height,
            fill=self.__color, outline=self.__color
        )