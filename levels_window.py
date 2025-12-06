import tkinter as tk


class LevelsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        btn_back = tk.Button(top_bar, text="← Назад", command=self.controller.show_menu)
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
                command=lambda lvl=level: self.controller.show_level(lvl)
            )
            btn.pack(pady=5)
