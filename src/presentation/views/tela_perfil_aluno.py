
import tkinter as tk


class TelaPerfilAluno(tk.Frame):
    def __init__(self, master, aluno):
        super().__init__(master, bg="#E6CCB6")

        self.master = master
        self.aluno = aluno

        titulo = tk.Label(
            self,
            text="Perfil do Aluno",
            font=("Segoe UI", 22, "bold"),
            bg="#E6CCB6",
            fg="#49372D"
        )
        titulo.pack(pady=25)

        quadro = tk.LabelFrame(
            self,
            text=" Dados Cadastrais ",
            font=("Segoe UI", 12, "bold"),
            bg="#E6CCB6",
            padx=30,
            pady=25
        )
        quadro.pack(fill="x", padx=100, pady=15)

        dados = [
            ("Nome:", aluno.get_nome()),
            ("Matrícula:", aluno.matricula or "Não informada"),
            ("CPF:", aluno.cpf or "Não informado"),
            ("Data de nascimento:", aluno.data_nascimento),
            ("Série:", aluno.serie),
            ("ID:", str(aluno.id)),
            (
                "Possui laudo:",
                "Sim" if aluno.tem_laudo else "Não"
            )
        ]

        for rotulo, valor in dados:
            linha = tk.Frame(quadro, bg="#E6CCB6")
            linha.pack(fill="x", pady=7)

            tk.Label(
                linha,
                text=rotulo,
                font=("Segoe UI", 11, "bold"),
                bg="#E6CCB6",
                fg="#49372D",
                width=22,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                linha,
                text=valor,
                font=("Segoe UI", 11),
                bg="#E6CCB6",
                fg="#49372D"
            ).pack(side="left")

        titulo_boletim = tk.Label(
            self,
            text="Boletim Escolar",
            font=("Segoe UI", 16, "bold"),
            bg="#E6CCB6",
            fg="#49372D"
        )
        titulo_boletim.pack(pady=(25, 5))

        tk.Label(
            self,
            text="As notas do aluno serão adicionadas nesta área.",
            font=("Segoe UI", 10),
            bg="#E6CCB6",
            fg="#49372D"
        ).pack(pady=5)

        btn_voltar = tk.Button(
            self,
            text="← Voltar para Alunos",
            command=lambda: master.mudar_tela(
                "Cadastro de Alunos"
            ),
            bg="#B06C4B",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            width=22,
            height=2
        )
        btn_voltar.pack(pady=25)
