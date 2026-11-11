import tkinter as tk # biblioteca pra fazer a interface


class BotaoPersonalizado(tk.Button): # classe 1
    def __init__(self, master=None, **kwargs): # kwargs keywords arguments recebe argumentos nomeados sem precisar declarar um de cada vez
        super().__init__(master, **kwargs)
        self.config(
            font=("Segoe UI", 12, "bold"),
            bg="#6A3A2A",
            fg="white",
            relief=tk.GROOVE,
            activebackground="#6A3A2A",
            activeforeground="white",
            height=1,
            width=20
        )

