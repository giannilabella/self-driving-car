import tkinter as tk

from car import Car

# Setting up Application Window
window = tk.Tk()
window.title('Self Driving Car')
window.state('zoomed')
window.update()

# Setting up Car Canvas
car_canvas = tk.Canvas(
    window,
    width=window.winfo_width(),
    height=window.winfo_height(),
    background='grey'
)
car_canvas.pack(side=tk.LEFT)

# Define Car
car = Car(
    window,
    window.winfo_width() / 2,
    window.winfo_height() / 2,
    45, 75, 'blue'
)

# Animate loop
while 1 :
    car.update()
    car.draw(car_canvas)
    
    window.update()