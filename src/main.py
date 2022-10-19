import tkinter
from car import Car

# Setting up Application Window
window = tkinter.Tk()
window.title('Self Driving Car')
window.state('zoomed')
window.update()

# Setting up Car Canvas
car_canvas = tkinter.Canvas(
    window,
    width=window.winfo_width(),
    height=window.winfo_height(),
    background='grey'
)
car_canvas.pack(side=tkinter.LEFT)

car = Car(
    window.winfo_width() / 2, window.winfo_height() / 2,
    100, 300, 'blue', window
)
car.draw(car_canvas)

window.mainloop()