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
    road.get_lane_center(1),
    car_initial_y,
    45, 75, 'AI', window
)
# Define Traffic
traffic = [
    Car(road.get_lane_center(1), window.winfo_height() * 0.15, 45, 75, 'DUMMY', max_speed = 3)
]

# Animation loop
def animate () :
    # Update Cars
    for vehicle in traffic :
        vehicle.update([], [])

    _, car_y_movement = car.update(road.borders, traffic)

    # Draw Cars
    for vehicle in traffic :
        vehicle_y = vehicle.y - car.y + car_initial_y
        vehicle.draw(car_canvas, 'darkorange', fixed_y = vehicle_y)

    car.draw(car_canvas, 'blue', fixed_y = car_initial_y)
    
    # Animate road
    road.animate_lines(car_canvas, car_y_movement)
    
    car_canvas.after(10, animate)

animate()
window.mainloop()