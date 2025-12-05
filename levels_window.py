import tkinter as tk


class LevelsWindow(tk.Toplevel):


    def __init__(self, master: tk.Tk):
        super().__init__(master)

        self.title("Выбор уровня")
        self.geometry("300x300")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._create_widgets()

    def _create_widgets(self):
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
        pass

    def on_close(self):
        self.destroy()
