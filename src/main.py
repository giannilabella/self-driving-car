import tkinter as tk

from car import Car
from road import Road

# Setting up Application Window
window = tk.Tk()
window.title('Self Driving Car')
window.state('zoomed')
window.update()

# Setting up Car Canvas
car_canvas_width = 250
car_canvas = tk.Canvas(
    window,
    width=car_canvas_width,
    height=window.winfo_height(),
    background='grey',
    yscrollincrement=1
)
car_canvas.pack()

# Define road
road = Road(car_canvas_width / 2, car_canvas_width * 0.9)
road.draw(car_canvas)
# Define Car
car = Car(
    window,
    road.get_lane_center(1),
    window.winfo_height() - 100,
    45, 75, 'blue'
)

# Animation loop
def animate () :
    y_movement = car.update()
    car_canvas.yview_scroll(-int(y_movement), what='units')
    car.draw(car_canvas)

    car_canvas.after(10, animate)

animate()
window.mainloop()