import tkinter as tk
from tkinter import messagebox
from pathlib import Path


class LevelWindow(tk.Toplevel):

    def __init__(self, master: tk.Toplevel, level: int):
        super().__init__(master)

        self.level = level
        self.expected_text: str = ""

        self.title(f"Уровень {level}")
        self.geometry("800x400")
        self.resizable(True, False)

        # обработчик закрытия окна (крестик)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._create_widgets()
        self._load_level_text()

    def _create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.label_text = tk.Label(
            frame,
            text="",
            font=("Arial", 14),
            wraplength=760,
            justify="left"
        )
        self.label_text.pack(pady=10)

        self.entry_input = tk.Entry(frame, font=("Arial", 14), width=70)
        self.entry_input.pack(pady=10)
        self.entry_input.focus_set()

    def _load_level_text(self):
        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir / "data"
        filename = data_dir / f"level{self.level}.txt"

        try:
            text = filename.read_text(encoding="utf-8").strip()
            if not text:
                text = f"(Файл {filename.name} пуст. Добавьте туда текст для уровня {self.level}.)"
        except FileNotFoundError:
            messagebox.showwarning(
                "Файл не найден",
                f"Не удалось найти файл {filename}.\n"
                f"Создайте его и добавьте текст для уровня {self.level}."
            )
            text = f"(Нет текста: файл level{self.level}.txt отсутствует.)"

        self.expected_text = text
        self.label_text.config(text=text)

    def on_close(self):
        self.destroy()
