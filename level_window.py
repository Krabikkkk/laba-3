import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import time
import json

# Класс для описания логики поведения самого тренажера на определенных уровнях

class LevelFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.level = 1
        self.expected_text = ""
        self.expected_lines = []
        self.start_time = None
        self.errors = 0
        self.finished = False
        self.score = 0
        self.best_score = None

        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        btn_back = tk.Button(top_bar, text="← Назад", command=self.go_to_levels)
        btn_back.pack(side="left",padx=5, pady=5)

        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.text_example = tk.Text(
            frame,
            font=("Arial", 14),
            width=70,
            height=1,
            wrap="none",
            borderwidth=0,
            highlightthickness=0
        )
        self.text_example.pack(pady=10, fill="x")
        self.text_example.configure(state="normal")

        self.text_example.tag_config("correct", background="#b8f5b1")
        self.text_example.tag_config("wrong", background="#f5b1b1")
        self.text_example.tag_config("cursor", underline=True)

        self.entry_input = tk.Text(
            frame,
            font=("Arial", 14),
            width=70,
            height=1,
            wrap="none"
        )
        self.entry_input.pack(pady=10, fill="x")
        self.entry_input.focus_set()

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

        self.btn_restart = tk.Button(
            buttons_frame,
            text="Начать сначала",
            command=self.restart_level
        )
        self.btn_restart.pack(side="left", padx=5)

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

# метод set_level для установки начальных настроек параметров при запуске уровня

    def set_level(self, level: int):
        self.level = level
        self.finished = False
        self.errors = 0
        self.score = 0
        self.start_time = None
        self.expected_text = ""
        self.expected_lines = []
        self.result_label.config(text="")
        if self.best_label.winfo_manager():
            self.best_label.pack_forget()
        self.btn_next_level.pack_forget()
        self.btn_levels.pack_forget()
        self.entry_input.delete("1.0", "end")
        self.entry_input.configure(height=1)
        self.entry_input.focus_set()
        self.status_label.config(text="Ошибки: 0 | Время: 0.0 c")

        self.text_example.configure(state="normal")
        self.text_example.delete("1.0", "end")
        self.text_example.configure(state="disabled")

        self._load_level_text()
        self._load_best_score()
        self.update_highlighting()

# аналогично set_level только при перезагрузке, выставляет меньше параметров в значения по умолчанию

    def restart_level(self):
        self.finished = False
        self.errors = 0
        self.score = 0
        self.start_time = None
        self.entry_input.delete("1.0", "end")
        self.entry_input.focus_set()
        self.status_label.config(text="Ошибки: 0 | Время: 0.0 c")
        self.result_label.config(text="")
        self.btn_next_level.pack_forget()
        self.btn_levels.pack_forget()
        self.update_highlighting()

# читаем текст для уровня из txt файла

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
        self.expected_lines = self.expected_text.split("\n")

        self.text_example.configure(state="normal")
        self.text_example.delete("1.0", "end")
        self.text_example.insert("1.0", self.expected_text)
        self.text_example.configure(state="disabled")

        lines = len(self.expected_lines)
        if lines < 1:
            lines = 1
        if lines > 10:
            lines = 10
        self.entry_input.configure(height=lines)
        self.text_example.configure(height=lines)

# Методы для работы с json файлом

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

# рассчет времени за которое пользователь прошел уровень

    def update_status(self):
        if self.start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - self.start_time
        self.status_label.config(
            text=f"Ошибки: {self.errors} | Время: {elapsed:.1f} c"
        )

# для перевода строк в нормальный вид

    def _index_to_global(self, line_index: int, col_index: int) -> int:
        offset = 0
        for i in range(line_index):
            offset += len(self.expected_lines[i])
            if i < len(self.expected_lines) - 1:
                offset += 1
        return offset + col_index

# обновление для текста

    def update_highlighting(self):
        current_text = self.entry_input.get("1.0", "end-1c")
        self.text_example.configure(state="normal")
        self.text_example.tag_remove("correct", "1.0", "end")
        self.text_example.tag_remove("wrong", "1.0", "end")
        self.text_example.tag_remove("cursor", "1.0", "end")

        max_len = min(len(current_text), len(self.expected_text))
        for i in range(max_len):
            exp_ch = self.expected_text[i]
            typed_ch = current_text[i]
            start = f"1.0 + {i} chars"
            end = f"1.0 + {i+1} chars"
            if typed_ch == exp_ch:
                self.text_example.tag_add("correct", start, end)
            else:
                self.text_example.tag_add("wrong", start, end)

        if len(current_text) < len(self.expected_text):
            start = f"1.0 + {len(current_text)} chars"
            end = f"1.0 + {len(current_text)+1} chars"
            self.text_example.tag_add("cursor", start, end)

        self.text_example.configure(state="disabled")

# метод для отслеживания действий пользователя на клавиатуре

    def on_key_press(self, event):
        if self.finished:
            return "break"

        if event.keysym == "BackSpace":
            return

        if not event.char and event.keysym != "Return":
            return "break"

        insert_index = self.entry_input.index("insert")
        end_index = self.entry_input.index("end-1c")
        if insert_index != end_index:
            return "break"

        index_str = insert_index
        line_str, col_str = index_str.split(".")
        line_idx = int(line_str) - 1
        col_idx = int(col_str)

        if line_idx >= len(self.expected_lines):
            return "break"

        if event.keysym == "Return":
            if line_idx >= len(self.expected_lines) - 1:
                return "break"
            if col_idx != len(self.expected_lines[line_idx]):
                return "break"
            typed_char = "\n"
        else:
            if col_idx >= len(self.expected_lines[line_idx]):
                return "break"
            typed_char = event.char

        if self.start_time is None:
            self.start_time = time.time()

        global_index = self._index_to_global(line_idx, col_idx)
        expected_char = self.expected_text[global_index]
        if typed_char != expected_char:
            self.errors += 1

        self.update_status()

# метод для проверки того закончился ли уровень

    def on_key_release(self, event):
        if self.finished:
            return
        self.update_highlighting()
        current_text = self.entry_input.get("1.0", "end-1c")
        if current_text == self.expected_text and len(current_text) == len(self.expected_text):
            self.finish_attempt()

# метод для расчета финальных характеристик(скорость пользователя, количетсво очков)

    def finish_attempt(self):
        self.finished = True
        if self.start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - self.start_time
        length = len(self.expected_text)
        speed = length / elapsed
        self.score = int(1000 + (length - elapsed) * 10 + (self.errors * -20))
        if self.score < 0:
            self.score = 0
        self.status_label.config(
            text=f"Ошибки: {self.errors} | Время: {elapsed:.1f} c"
        )
        self.result_label.config(
            text=f"Очки: {self.score}\nСредняя скорость: {speed:.1f} симв/сек"
        )
        if self.best_score is None or self.score > self.best_score:
            self.best_score = self.score
            self._save_best_score()
        if self.best_score is not None:
            self.best_label.config(text=f"Лучший результат: {self.best_score}")
            self.best_label.pack(pady=2)
        if self.level < 5:
            self.btn_next_level.pack(side="left", padx=5)
        self.btn_levels.pack(side="left", padx=5)

# метод для перехода на следующий уровень

    def go_next_level(self):
        if self.level < 5:
            self.controller.show_level(self.level + 1)

# метод для перехода к меню уровней

    def go_to_levels(self):
        self.controller.show_levels()
