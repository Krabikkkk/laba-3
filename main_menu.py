import tkinter as tk
from tkinter import messagebox

from levels_window import LevelsWindow


class MainMenuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Клавиатурный тренажёр — меню")
        self.window_width = 800
        self.window_height = 400
        self.center_window(self.window_width, self.window_height)
        self.resizable(True, True)
        self.bind("<Configure>", self.on_resize)
        self._create_widgets()

    def center_window(self, width, height):
        self.geometry(f"{width}x{height}")
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_resize(self, event):
        if event.widget is self and event.width > 1 and event.height > 1:
            self.window_width = event.width
            self.window_height = event.height

    def _create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(expand=True)

        btn_play = tk.Button(frame, text="Играть", width=20, command=self.on_play)
        btn_play.pack(pady=10)

        btn_help = tk.Button(frame, text="Справка", width=20, command=self.on_help)
        btn_help.pack(pady=10)

        btn_exit = tk.Button(frame, text="Выход", width=20, command=self.on_exit)
        btn_exit.pack(pady=10)

    def on_play(self):
        self.withdraw()
        LevelsWindow(self)

    def on_help(self):
        messagebox.showinfo("Справка", "Клавиатурный тренажер версия 1.0")

    def on_exit(self):
        self.destroy()
