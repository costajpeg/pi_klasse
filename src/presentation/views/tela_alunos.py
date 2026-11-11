import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.exceptions import ValidationError
from src.domain.utils import corresponde_busca


class TelaCadastroAlunos(tk.Frame): # classe 4
    def __init__(self, master): # master eh a janela principal
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.cadastrar_aluno_uc = master.cadastrar_aluno_uc
        self.listar_alunos_uc = master.listar_alunos_uc

        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Alunos", font=("Segoe UI", 18, "bold"), bg="#E6CCB6")
        lbl_titulo.pack(pady=15)

        container_divisao = tk.Frame(self, bg="#E6CCB6")
        container_divisao.pack(fill="both", expand=True, padx=30)

        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=2)
        container_divisao.rowconfigure(0, weight=1)

        # LADO ESQUERDO: FORMULÁRIO BASEADO NA TABELA ALUNOS
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Aluno ", font=("Segoe UI", 11, "bold"), bg="#E6CCB6", padx=15, pady=10)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        tk.Label(lado_esquerdo, text="Nome Completo:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 1))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_nome.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="Matrícula (opcional se quiser gerar aut.):", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_matricula = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_matricula.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="CPF (opcional se quiser gerar aut.):", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_cpf = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_cpf.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="Data de Nasc. (DD/MM/AAAA ou AAAA-MM-DD):", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.txt_nascimento = tk.Entry(lado_esquerdo, font=("Segoe UI", 10))
        self.txt_nascimento.insert(0, "15/03/2014")
        self.txt_nascimento.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="Série Atual:", bg="#E6CCB6", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 1))
        self.cb_serie = ttk.Combobox(lado_esquerdo, values=self.master.series_predefinidas, font=("Segoe UI", 10), state="readonly")
        self.cb_serie.pack(fill="x", pady=(0, 15))
        self.cb_serie.current(0)

        btn_salvar = tk.Button(lado_esquerdo, text="Adicionar Aluno", command=self.adicionar_aluno, bg="#B06C4B", fg="white", relief=tk.FLAT, font=("Segoe UI", 10, "bold"), height=2)
        btn_salvar.pack(fill="x")

        # LADO DIREITO: LISTA DOS ALUNOS
        lado_direito = tk.LabelFrame(container_divisao, text=" Alunos Registrados no Banco ", font=("Segoe UI", 11, "bold"), bg="#E6CCB6", padx=15, pady=10)
        lado_direito.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        # Barra de pesquisa por correspondência
        frame_pesquisa = tk.Frame(lado_direito, bg="#E6CCB6")
        frame_pesquisa.pack(fill="x", pady=(0, 6))

        tk.Label(frame_pesquisa, text="🔍 Buscar aluno:", font=("Segoe UI", 9, "bold"), bg="#E6CCB6").pack(side="left")
        self.txt_busca = tk.Entry(frame_pesquisa, font=("Segoe UI", 10))
        self.txt_busca.pack(side="left", fill="x", expand=True, padx=6)
        self.txt_busca.bind("<KeyRelease>", lambda e: self.atualizar_tabela_alunos())

        btn_limpar_busca = tk.Button(frame_pesquisa, text="↺", command=self.limpar_busca, bg="#D2A27F", fg="white", relief=tk.FLAT, font=("Segoe UI", 8, "bold"), width=3)
        btn_limpar_busca.pack(side="right")

        colunas = ("id", "matricula", "cpf", "nome", "nascimento", "serie")
        self.tabela = ttk.Treeview(lado_direito, columns=colunas, show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("matricula", text="Matrícula")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("nome", text="Nome do Aluno")
        self.tabela.heading("nascimento", text="Nascimento")
        self.tabela.heading("serie", text="Série")

        self.tabela.column("id", width=45, minwidth=40, anchor="center")
        self.tabela.column("matricula", width=80, minwidth=70, anchor="center")
        self.tabela.column("cpf", width=110, minwidth=90, anchor="center")
        self.tabela.column("nome", width=160, minwidth=120, anchor="w")
        self.tabela.column("nascimento", width=95, minwidth=85, anchor="center")
        self.tabela.column("serie", width=80, minwidth=70, anchor="center")

        scrollbar = ttk.Scrollbar(lado_direito, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        self.atualizar_tabela_alunos()

        # BOTAO VOLTAR
        btn_voltar = tk.Button(self, text="← Voltar ao Menu Principal", font=("Segoe UI", 10), command=master.mostrar_menu, bg="#D2A27F", fg="white", relief=tk.FLAT, width=22, height=1)
        btn_voltar.pack(pady=15)

    def atualizar_tabela_alunos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        termo = self.txt_busca.get().strip()
        todos_alunos = self.listar_alunos_uc.executar()

        for aluno in todos_alunos:
            if corresponde_busca(termo, aluno.get_nome(), aluno.matricula, aluno.cpf, aluno.serie):
                self.tabela.insert("", "end", values=(
                    aluno.id,
                    aluno.matricula,
                    aluno.cpf,
                    aluno.get_nome(),
                    aluno.data_nascimento,
                    aluno.serie
                ))

    def limpar_busca(self):
        self.txt_busca.delete(0, tk.END)
        self.atualizar_tabela_alunos()

    def adicionar_aluno(self):
        nome = self.txt_nome.get().strip()
        matricula = self.txt_matricula.get().strip()
        cpf = self.txt_cpf.get().strip()
        nasc = self.txt_nascimento.get().strip()
        serie = self.cb_serie.get()

        try:
            self.cadastrar_aluno_uc.executar(
                nome=nome,
                serie=serie,
                matricula=matricula,
                cpf=cpf,
                data_nascimento=nasc
            )
            self.atualizar_tabela_alunos()
            self.txt_nome.delete(0, tk.END)
            self.txt_matricula.delete(0, tk.END)
            self.txt_cpf.delete(0, tk.END)
        except ValidationError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
