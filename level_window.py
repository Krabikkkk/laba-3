import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import time
import json


class LevelFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.level = 1
        self.expected_text = ""
        self.start_time = None
        self.errors = 0
        self.finished = False
        self.score = 0
        self.best_score = None

        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        btn_back = tk.Button(top_bar, text="← Назад", command=self.go_to_levels)
        btn_back.pack(side="left", padx=5, pady=5)

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

        self.status_label = tk.Label(
            frame,
            text="Ошибки: 0 | Время: 0.0 c",
            font=("Arial", 12),
            justify="left"
        )
        self.status_label.pack(pady=5, anchor="w")

        self.result_label = tk.Label(frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=5)

        self.best_label = tk.Label(frame, text="", font=("Arial", 12))

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(pady=10)

        self.btn_next_level = tk.Button(
            buttons_frame,
            text="Следующий уровень",
            command=self.go_next_level
        )
        self.btn_levels = tk.Button(
            buttons_frame,
            text="Уровни",
            command=self.go_to_levels
        )

        self.entry_input.bind("<KeyPress>", self.on_key_press)
        self.entry_input.bind("<KeyRelease>", self.on_key_release)

    def set_level(self, level: int):
        self.level = level
        self.finished = False
        self.errors = 0
        self.score = 0
        self.start_time = None
        self.expected_text = ""
        self.result_label.config(text="")
        if self.best_label.winfo_manager():
            self.best_label.pack_forget()
        self.btn_next_level.pack_forget()
        self.btn_levels.pack_forget()
        self.entry_input.delete(0, tk.END)
        self.entry_input.focus_set()
        self.status_label.config(text="Ошибки: 0 | Время: 0.0 c")
        self._load_level_text()
        self._load_best_score()

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
            text = f"(Нет текста для уровня {self.level})"

        self.expected_text = text
        self.label_text.config(text=text)

    def _best_scores_file(self) -> Path:
        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir / "best_scores.json"

    def _load_best_score(self):
        file_path = self._best_scores_file()
        if not file_path.exists():
            self.best_score = None
            return
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            key = f"level_{self.level}"
            value = data.get(key)
            if isinstance(value, int):
                self.best_score = value
            else:
                self.best_score = None
        except (OSError, json.JSONDecodeError):
            self.best_score = None

    def _save_best_score(self):
        file_path = self._best_scores_file()
        data = {}
        if file_path.exists():
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    data = loaded
            except (OSError, json.JSONDecodeError):
                data = {}
        key = f"level_{self.level}"
        data[key] = self.best_score
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_status(self):
        if self.start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - self.start_time
        self.status_label.config(
            text=f"Ошибки: {self.errors} | Время: {elapsed:.1f} c"
        )

    def on_key_press(self, event):
        if self.finished:
            return
        if not event.char:
            return
        if event.keysym == "BackSpace":
            return
        if self.start_time is None:
            self.start_time = time.time()
        current_text = self.entry_input.get()
        index = len(current_text)
        if index >= len(self.expected_text):
            self.errors += 1
        else:
            expected_char = self.expected_text[index]
            if event.char != expected_char:
                self.errors += 1
        self.update_status()

    def on_key_release(self, event):
        if self.finished:
            return
        current_text = self.entry_input.get()
        if current_text == self.expected_text and len(current_text) == len(self.expected_text):
            self.finish_attempt()

    def finish_attempt(self):
        self.finished = True
        if self.start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - self.start_time
        length = len(self.expected_text)
        self.score = int(1000 + (length - elapsed) * 10 + (self.errors * -20))
        if self.score < 0:
            self.score = 0
        self.status_label.config(
            text=f"Ошибки: {self.errors} | Время: {elapsed:.1f} c"
        )
        self.result_label.config(text=f"Очки: {self.score}")
        if self.best_score is None or self.score > self.best_score:
            self.best_score = self.score
            self._save_best_score()
        if self.best_score is not None:
            self.best_label.config(text=f"Лучший результат: {self.best_score}")
            self.best_label.pack(pady=2)
        if self.level < 5:
            self.btn_next_level.pack(side="left", padx=5)
        self.btn_levels.pack(side="left", padx=5)

    def go_next_level(self):
        if self.level < 5:
            self.controller.show_level(self.level + 1)

    def go_to_levels(self):
        self.controller.show_levels()
