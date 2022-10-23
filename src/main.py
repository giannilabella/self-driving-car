import tkinter as tk

from car import Car
from road import Road
from visualizer import Visualizer

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
    background = 'grey',
    highlightthickness = 0
)
# Setting up Visualizer Canvas
visualizer_canvas = tk.Canvas(
    window,
    width = 700,
    height = window.winfo_height(),
    background = 'black',
    highlightthickness = 0
)

# Organize Canvas
visualizer_canvas.pack(side = tk.RIGHT, padx = (20, 0))
car_canvas.pack(side = tk.RIGHT, padx = (50, 20))

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
    45, 75, 'blue', 'AI', window
)
# Define Traffic
distance = 400
traffic = [
    Car(road.get_lane_center(0), car_initial_y - distance, 45, 75, 'darkred', 'DUMMY', max_speed = 2.5),
    Car(road.get_lane_center(1), car_initial_y - distance, 45, 75, 'darkgreen', 'DUMMY', max_speed = 2.5),
    Car(road.get_lane_center(1), car_initial_y - 2 * distance, 45, 75, 'darkblue', 'DUMMY', max_speed = 2.8),
    Car(road.get_lane_center(2), car_initial_y - 2 * distance, 45, 75, 'darkorange', 'DUMMY', max_speed = 2.8),
    Car(road.get_lane_center(1), car_initial_y - 3 * distance, 45, 75, 'purple', 'DUMMY', max_speed = 3),
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
        vehicle.draw(car_canvas, fixed_y = vehicle_y)

    car.draw(car_canvas, fixed_y = car_initial_y)
    
    # Animate road
    road.animate_lines(car_canvas, car_y_movement)

    # Draw Visualizer
    if car.brain is not None :
        Visualizer.draw_network(visualizer_canvas, car.brain)
    
    window.after(10, animate)

animate()
window.mainloop()