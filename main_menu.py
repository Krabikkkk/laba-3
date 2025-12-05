import tkinter as tk


class MainMenuApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Клавиатурный тренажёр — меню")
        self.geometry("400x300")
        self.resizable(False, False)

        self._create_widgets()

    def _create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(expand=True)

        btn_play = tk.Button(
            frame,
            text="Играть",
            width=20,
            command=self.on_play
        )
        btn_play.pack(pady=10)

        btn_help = tk.Button(
            frame,
            text="Справка",
            width=20,
            command=self.on_help
        )
        btn_help.pack(pady=10)

        btn_exit = tk.Button(
            frame,
            text="Выход",
            width=20,
            command=self.on_exit
        )
        btn_exit.pack(pady=10)


    def on_play(self):
        pass

    def on_help(self):
        pass

    def on_exit(self):
        self.destroy()
