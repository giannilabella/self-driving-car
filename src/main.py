import tkinter as tk

from car import Car
from road import Road

# Setting up Application Window
window = tk.Tk()
window.title('Self Driving Car')
window.state('zoomed')

# Force update on width and height for windows after maximize
window.update()

# Setting up Car Canvas
car_canvas_width = 250
car_canvas = tk.Canvas(
    window,
    width = car_canvas_width,
    height = window.winfo_height(),
    background = 'grey'
)
car_canvas.pack()

# Force update on width and height for canvas
window.update()

# Define road
road = Road(car_canvas_width / 2, car_canvas_width * 0.9)
road.draw(car_canvas)
# Define Car
car_initial_y = window.winfo_height() * 0.85
car = Car(
    window,
    road.get_lane_center(1),
    car_initial_y,
    45, 75, 'blue'
)

# Animation loop
def animate () :
    _, car_y_movement = car.update(road.borders)
    car.draw(car_canvas, car_initial_y)
    
    road.animate_lines(car_canvas, car_y_movement)
    
    car_canvas.after(10, animate)

animate()
window.mainloop()