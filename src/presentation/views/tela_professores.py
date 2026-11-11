import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.exceptions import ValidationError


class TelaCadastroProfessores(tk.Frame): # classe 5
    def __init__(self, master):
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.cadastrar_professor_uc = master.cadastrar_professor_uc
        self.listar_professores_uc = master.listar_professores_uc

        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Professores", font=("Segoe UI", 18, "bold"), bg="#E6CCB6")
        lbl_titulo.pack(pady=15)

        container_divisao = tk.Frame(self, bg="#E6CCB6")
        container_divisao.pack(fill="both", expand=True, padx=30)

        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=2)
        container_divisao.rowconfigure(0, weight=1)

        # LADO ESQUERDO: FORMULÁRIO BASEADO NA TABELA PROFESSORES
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Professor ", font=("Segoe UI", 11, "bold"), bg="#E6CCB6", padx=15, pady=10)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        tk.Label(lado_esquerdo, text="Nome Completo:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 1))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_nome.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="Matrícula:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_matricula = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_matricula.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="CPF:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_cpf = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_cpf.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="E-mail Institucional:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_email = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_email.pack(fill="x", pady=(0, 15))

        btn_salvar = tk.Button(lado_esquerdo, text="Adicionar Professor", command=self.adicionar_professor, bg="#B06C4B", fg="white", relief=tk.FLAT, font=("Segoe UI", 10, "bold"), height=2)
        btn_salvar.pack(fill="x")

        # LADO DIREITO: LISTA DOS PROFESSORES
        lado_direito = tk.LabelFrame(container_divisao, text=" Professores Registrados no Banco ", font=("Segoe UI", 11, "bold"), bg="#E6CCB6", padx=15, pady=10)
        lado_direito.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        colunas = ("id", "matricula", "cpf", "nome", "email")
        self.tabela = ttk.Treeview(lado_direito, columns=colunas, show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("matricula", text="Matrícula")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("nome", text="Nome do Professor")
        self.tabela.heading("email", text="E-mail")

        self.tabela.column("id", width=45, minwidth=40, anchor="center")
        self.tabela.column("matricula", width=80, minwidth=70, anchor="center")
        self.tabela.column("cpf", width=110, minwidth=90, anchor="center")
        self.tabela.column("nome", width=170, minwidth=130, anchor="w")
        self.tabela.column("email", width=190, minwidth=140, anchor="w")

        scrollbar = ttk.Scrollbar(lado_direito, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        for professor in self.listar_professores_uc.executar():
            self.tabela.insert("", "end", values=(
                professor.id,
                professor.matricula,
                professor.cpf,
                professor.get_nome(),
                professor.email
            ))

        btn_voltar = tk.Button(self, text="← Voltar ao Menu Principal", font=("Segoe UI", 10), command=master.mostrar_menu, bg="#D2A27F", fg="white", relief=tk.FLAT, width=22, height=1)
        btn_voltar.pack(pady=15)

    def adicionar_professor(self):
        nome = self.txt_nome.get().strip()
        matricula = self.txt_matricula.get().strip()
        cpf = self.txt_cpf.get().strip()
        email = self.txt_email.get().strip()

        try:
            prof = self.cadastrar_professor_uc.executar(
                nome=nome,
                matricula=matricula,
                email=email,
                cpf=cpf
            )
            self.tabela.insert("", "end", values=(
                prof.id,
                prof.matricula,
                prof.cpf,
                prof.get_nome(),
                prof.email
            ))

            self.txt_nome.delete(0, tk.END)
            self.txt_matricula.delete(0, tk.END)
            self.txt_cpf.delete(0, tk.END)
            self.txt_email.delete(0, tk.END)
        except ValidationError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
