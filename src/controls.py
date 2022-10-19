from tkinter import Tk, Event

class Controls :
    def __init__(self, window: Tk) -> None:
        self.__forward = False
        self.__left = False
        self.__right = False
        self.__reverse = False
        
        self.__add_keyboard_listeners(window)
        
    def __handle_key_press (self, event: Event) :
        match (event.keysym) :
            case 'Up' : self.__forward = True
            case 'Left' : self.__left = True
            case 'Right' : self.__right = True
            case 'Down' : self.__reverse = True
    
    def __handle_key_release (self, event) :
        match (event.keysym) :
            case 'Up' : self.__forward = False
            case 'Left' : self.__left = False
            case 'Right' : self.__right = False
            case 'Down' : self.__reverse = False
        
    def __add_keyboard_listeners (self, window: Tk) :
        key_press, key_release = '<KeyPress>', '<KeyRelease>'
        window.bind(key_press, self.__handle_key_press)
        window.bind(key_release, self.__handle_key_release)