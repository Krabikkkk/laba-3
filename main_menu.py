import tkinter as tk
from tkinter import messagebox

from levels_window import LevelsFrame
from level_window import LevelFrame

# Класс реализуйющй логику общего окна, запускает весь интерфейс

class MainMenuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Клавиатурный тренажёр")
        self._center_window(800, 400)
        self.resizable(True, True)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.container = container

        self.menu_frame = MainMenuFrame(container, controller=self)
        self.levels_frame = LevelsFrame(container, controller=self)
        self.level_frame = LevelFrame(container, controller=self)

        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.levels_frame.grid(row=0, column=0, sticky="nsew")
        self.level_frame.grid(row=0, column=0, sticky="nsew")

        self.show_menu()


    def _center_window(self, width, height):
        self.geometry(f"{width}x{height}")
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

# методы для перехода на другие окна

    def show_menu(self):
        self.menu_frame.tkraise()

    def show_levels(self):
        self.levels_frame.tkraise()

    def show_level(self, level: int):
        self.level_frame.set_level(level)
        self.level_frame.tkraise()


# Класс реализуйющй логику для основного меню

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller: MainMenuApp):
        super().__init__(parent)
        self.controller = controller

        frame = tk.Frame(self)
        frame.pack(expand=True)

        btn_play = tk.Button(frame, text="Играть", width=20, command=self.controller.show_levels)
        btn_play.pack(pady=10)

        btn_help = tk.Button(frame, text="Справка", width=20, command=self.show_help)
        btn_help.pack(pady=10)

        btn_exit = tk.Button(frame, text="Выход", width=20, command=self.controller.destroy)
        btn_exit.pack(pady=10)

    def show_help(self):
        messagebox.showinfo("Справка", "Клавиатурный тренажер версия 1.0")
