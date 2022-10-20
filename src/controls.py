import tkinter as tk

class Controls :
    def __init__ (self, window: tk.Tk) -> None:
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False
        
        self.__add_keyboard_listeners(window)
        
    def __handle_key_press (self, event: tk.Event) :
        match (event.keysym) :
            case 'Up' : self.forward = True
            case 'Left' : self.left = True
            case 'Right' : self.right = True
            case 'Down' : self.reverse = True
    
    def __handle_key_release (self, event) :
        match (event.keysym) :
            case 'Up' : self.forward = False
            case 'Left' : self.left = False
            case 'Right' : self.right = False
            case 'Down' : self.reverse = False
        
    def __add_keyboard_listeners (self, window: tk.Tk) :
        key_press, key_release = '<KeyPress>', '<KeyRelease>'
        window.bind(key_press, self.__handle_key_press)
        window.bind(key_release, self.__handle_key_release)