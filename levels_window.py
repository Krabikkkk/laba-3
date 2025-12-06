import tkinter as tk

from level_window import LevelWindow


class LevelsWindow(tk.Toplevel):
    def __init__(self, main_app: tk.Tk):
        super().__init__(main_app)
        self.main_app = main_app
        self.title("Выбор уровня")
        self.center_window(self.main_app.window_width, self.main_app.window_height)
        self.resizable(True, True)
        self.bind("<Configure>", self.on_resize)
        self.protocol("WM_DELETE_WINDOW", self.back_to_menu)
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
            self.main_app.window_width = event.width
            self.main_app.window_height = event.height

    def _create_widgets(self):
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        btn_back = tk.Button(top_bar, text="← Назад", command=self.back_to_menu)
        btn_back.pack(side="left", padx=5, pady=5)

        frame = tk.Frame(self)
        frame.pack(expand=True)

        label = tk.Label(frame, text="Выберите уровень", font=("Arial", 14))
        label.pack(pady=10)

        for level in range(1, 6):
            btn = tk.Button(
                frame,
                text=f"Уровень {level}",
                width=20,
                command=lambda lvl=level: self.on_level_click(lvl)
            )
            btn.pack(pady=5)

    def on_level_click(self, level: int):
        def back_callback():
            LevelsWindow(self.main_app)
        self.destroy()
        LevelWindow(self.main_app, level, on_back=back_callback)

    def back_to_menu(self):
        self.destroy()
        self.main_app.center_window(self.main_app.window_width, self.main_app.window_height)
        self.main_app.deiconify()
