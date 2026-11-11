import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.utils import corresponde_busca


class TelaHistoricoAlunosTurmas(tk.Frame):
    """Tela para consulta e acompanhamento do histórico escolar de alunos em turmas."""
    def __init__(self, master):
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.listar_historico_uc = master.listar_historico_uc
        self.listar_alunos_uc = master.listar_alunos_uc

        lbl_titulo = tk.Label(
            self,
            text="Histórico Escolar: Alunos e Turmas",
            font=("Segoe UI", 18, "bold"),
            bg="#E6CCB6"
        )
        lbl_titulo.pack(pady=10)

        # PAINEL SUPERIOR: FILTROS DE CONSULTA
        frame_filtros = tk.LabelFrame(
            self,
            text=" Pesquisa Rápida e Filtros ",
            font=("Segoe UI", 11, "bold"),
            bg="#E6CCB6",
            padx=15,
            pady=8
        )
        frame_filtros.pack(fill="x", padx=30, pady=5)

        for col in range(4):
            frame_filtros.columnconfigure(col, weight=1)

        # 1. Busca flexível por Aluno (Nome ou Matrícula)
        tk.Label(
            frame_filtros,
            text="Buscar Aluno (ex: 'thais paixão', 'noah', matrícula):",
            font=("Segoe UI", 10, "bold"),
            bg="#E6CCB6"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=5)

        self.txt_busca_aluno = tk.Entry(frame_filtros, font=("Segoe UI", 10))
        self.txt_busca_aluno.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))
        # Filtra automaticamente em tempo real conforme o usuário digita
        self.txt_busca_aluno.bind("<KeyRelease>", lambda e: self.carregar_dados())

        # 2. Filtro por Série
        tk.Label(frame_filtros, text="Filtrar por Série:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=2, sticky="w", padx=5)
        opcoes_serie = ["Todas"] + list(self.master.series_predefinidas)
        self.cb_serie = ttk.Combobox(frame_filtros, values=opcoes_serie, state="readonly", font=("Segoe UI", 10))
        self.cb_serie.current(0)
        self.cb_serie.grid(row=1, column=2, sticky="ew", padx=5, pady=(2, 5))
        self.cb_serie.bind("<<ComboboxSelected>>", lambda e: self.carregar_dados())

        # 3. Filtro por Ano Letivo
        tk.Label(frame_filtros, text="Ano Letivo:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=3, sticky="w", padx=5)
        frame_ano_acoes = tk.Frame(frame_filtros, bg="#E6CCB6")
        frame_ano_acoes.grid(row=1, column=3, sticky="ew", padx=5, pady=(2, 5))

        self.txt_ano_letivo = tk.Entry(frame_ano_acoes, font=("Segoe UI", 10), width=8)
        self.txt_ano_letivo.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.txt_ano_letivo.bind("<KeyRelease>", lambda e: self.carregar_dados())

        btn_limpar = tk.Button(
            frame_ano_acoes,
            text="↺ Limpar",
            command=self.limpar_filtros,
            bg="#D2A27F",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=8
        )
        btn_limpar.pack(side="right")

        # PAINEL CENTRAL: TABELA DE HISTÓRICO
        frame_tabela = tk.Frame(self, bg="#E6CCB6")
        frame_tabela.pack(fill="both", expand=True, padx=30, pady=6)

        self.lbl_contador = tk.Label(frame_tabela, text="Carregando histórico...", font=("Segoe UI", 10, "bold"), bg="#E6CCB6")
        self.lbl_contador.pack(anchor="w", pady=(0, 4))

        colunas = ("id", "ano_letivo", "serie", "matricula", "aluno", "turma")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("ano_letivo", text="Ano Letivo")
        self.tabela.heading("serie", text="Série")
        self.tabela.heading("matricula", text="Matrícula")
        self.tabela.heading("aluno", text="Nome do Aluno")
        self.tabela.heading("turma", text="Turma Vinculada")

        self.tabela.column("id", width=55, minwidth=40, anchor="center")
        self.tabela.column("ano_letivo", width=90, minwidth=80, anchor="center")
        self.tabela.column("serie", width=90, minwidth=80, anchor="center")
        self.tabela.column("matricula", width=110, minwidth=90, anchor="center")
        self.tabela.column("aluno", width=290, minwidth=180, anchor="w")
        self.tabela.column("turma", width=200, minwidth=140, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        # PAINEL INFERIOR: BOTÃO VOLTAR
        btn_voltar = tk.Button(
            self,
            text="← Voltar ao Menu Principal",
            font=("Segoe UI", 10),
            command=master.mostrar_menu,
            bg="#D2A27F",
            fg="white",
            relief=tk.FLAT,
            width=24,
            height=1
        )
        btn_voltar.pack(pady=10)

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        serie_filtro = self.cb_serie.get()
        ano_txt = self.txt_ano_letivo.get().strip()
        termo_busca = self.txt_busca_aluno.get().strip()

        ano_num = None
        if ano_txt:
            try:
                ano_num = int(ano_txt)
            except ValueError:
                self.lbl_contador.config(text="⚠️ Ano letivo deve ser numérico.")
                return

        try:
            # 1. Busca registros no histórico
            registros = self.listar_historico_uc.executar(
                ano_letivo=ano_num,
                serie=serie_filtro
            )

            # 2. Se há termo de busca, filtra por correspondência flexível (bag-of-words)
            if termo_busca:
                registros_filtrados = [
                    r for r in registros
                    if corresponde_busca(
                        termo_busca,
                        r.aluno_nome,
                        r.aluno_matricula,
                        r.turma_nome,
                        r.serie
                    )
                ]

                # Se não encontrou na série selecionada, busca em todas as séries
                if not registros_filtrados and serie_filtro != "Todas":
                    todos_registros = self.listar_historico_uc.executar(ano_letivo=ano_num, serie="Todas")
                    encontrados_outra_serie = [
                        r for r in todos_registros
                        if corresponde_busca(
                            termo_busca,
                            r.aluno_nome,
                            r.aluno_matricula,
                            r.turma_nome,
                            r.serie
                        )
                    ]
                    if encontrados_outra_serie:
                        registros_filtrados = encontrados_outra_serie
                        self.cb_serie.current(0) # Ajusta visualmente para 'Todas'

                registros = registros_filtrados

            # 3. Insere os registros de histórico encontrados
            for r in registros:
                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        r.id or "-",
                        r.ano_letivo,
                        r.serie,
                        r.aluno_matricula or "-",
                        r.aluno_nome or f"Aluno ID {r.aluno_id}",
                        r.turma_nome or f"Turma ID {r.turma_id}"
                    )
                )

            # 4. Caso o histórico esteja vazio para essa busca, verifica se o aluno está cadastrado no sistema
            if not registros and termo_busca:
                alunos_cadastrados = self.listar_alunos_uc.executar()
                alunos_sem_turma = [
                    a for a in alunos_cadastrados
                    if corresponde_busca(termo_busca, a.get_nome(), a.matricula, a.cpf, a.serie)
                ]

                if alunos_sem_turma:
                    for a in alunos_sem_turma:
                        self.tabela.insert(
                            "",
                            "end",
                            values=(
                                a.id or "-",
                                ano_num or "Atual",
                                a.serie,
                                a.matricula or "-",
                                a.get_nome(),
                                "(Aguardando sorteio de turma)"
                            )
                        )
                    nomes_encontrados = ", ".join([a.get_nome() for a in alunos_sem_turma])
                    self.lbl_contador.config(
                        text=f"ℹ️ Aluno(a) '{nomes_encontrados}' cadastrado(a), mas ainda aguarda sorteio de turma."
                    )
                    return

            total = len(registros)
            if termo_busca:
                self.lbl_contador.config(
                    text=f"Resultado da busca por '{termo_busca}': {total} registro(s) encontrado(s)."
                )
            else:
                self.lbl_contador.config(
                    text=f"Total de registros no histórico: {total}"
                )
        except Exception as e:
            self.lbl_contador.config(text="Erro ao carregar histórico.")
            messagebox.showerror("Erro", f"Falha ao consultar histórico: {e}")

    def limpar_filtros(self):
        self.cb_serie.current(0)
        self.txt_ano_letivo.delete(0, tk.END)
        self.txt_busca_aluno.delete(0, tk.END)
        self.carregar_dados()
