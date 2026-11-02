import tkinter as tk


class TelaBase(tk.Frame): # classe 2
    # usamos tk.Frame para as telas, pois ele deixa com q agrupamos botoes, tabelas, textos, em uma msm janela
    # tk.Frame eh tipo uma "caixinha"/container
    def __init__(self, master, titulo_texto: str, **kwargs):
        super().__init__(master, bg="#E6CCB6", **kwargs)
        label = tk.Label(self, text=titulo_texto, font=("Segoe UI", 18, "bold"), bg="#E6CCB6")
        label.pack(pady=40)
        btn_voltar = tk.Button(
            self,
            text="← Voltar ao Menu",
            font=("Segoe UI", 10),
            command=master.mostrar_menu,
            bg="#D2A27F",
            fg="white",
            relief=tk.FLAT
        )
        btn_voltar.pack(pady=10)

