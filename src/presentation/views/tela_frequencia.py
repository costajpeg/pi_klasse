import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from src.domain.exceptions import ValidationError


class TelaFrequencia(tk.Frame):
    """Tela para registro e consulta de frequência/chamada dos alunos."""
    def __init__(self, master):
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.listar_turmas_uc = master.listar_turmas_uc
        self.listar_alunos_uc = master.listar_alunos_uc
        self.listar_professores_uc = master.listar_professores_uc
        self.registrar_frequencia_uc = master.registrar_frequencia_uc
        self.listar_frequencias_uc = master.listar_frequencias_uc

        # Estado da chamada atual: lista de dicionários {"aluno": aluno_obj, "presente": True}
        self.alunos_chamada: list[dict] = []
        self.turmas_carregadas = self.listar_turmas_uc.executar(apenas_com_alunos=True)
        self.professores_cadastrados = self.listar_professores_uc.executar()
        self.mapa_alunos = {a.get_nome(): a for a in self.listar_alunos_uc.executar()}

        lbl_titulo = tk.Label(self, text="Registro de Frequência Escolar", font=("Segoe UI", 18, "bold"), bg="#E6CCB6")
        lbl_titulo.pack(pady=10)

        # PAINEL SUPERIOR: FILTROS E CONFIGURAÇÃO DA AULA
        frame_topo = tk.LabelFrame(self, text=" Dados da Chamada ", font=("Segoe UI", 11, "bold"), bg="#E6CCB6", padx=15, pady=8)
        frame_topo.pack(fill="x", padx=25, pady=5)

        for col in range(4):
            frame_topo.columnconfigure(col, weight=1)

        # 1. Seleção de Turma
        tk.Label(frame_topo, text="Turma:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=0, sticky="w", padx=5)
        self.nomes_turmas = [f"{t.nome} (Ano: {t.ano_letivo})" for t in self.turmas_carregadas]
        self.cb_turma = ttk.Combobox(frame_topo, values=self.nomes_turmas, state="readonly", font=("Segoe UI", 10))
        self.cb_turma.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 5))
        self.cb_turma.bind("<<ComboboxSelected>>", self.ao_selecionar_turma)

        # 2. Data da Chamada
        tk.Label(frame_topo, text="Data (DD/MM/AAAA):", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=1, sticky="w", padx=5)
        self.txt_data = tk.Entry(frame_topo, font=("Segoe UI", 10))
        hoje_formatado = datetime.date.today().strftime("%d/%m/%Y")
        self.txt_data.insert(0, hoje_formatado)
        self.txt_data.grid(row=1, column=1, sticky="ew", padx=5, pady=(2, 5))

        # 3. Disciplina
        tk.Label(frame_topo, text="Disciplina:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=2, sticky="w", padx=5)
        self.txt_disciplina = tk.Entry(frame_topo, font=("Segoe UI", 10))
        self.txt_disciplina.insert(0, "Regência")
        self.txt_disciplina.grid(row=1, column=2, sticky="ew", padx=5, pady=(2, 5))

        # 4. Professor
        tk.Label(frame_topo, text="Professor Regente:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").grid(row=0, column=3, sticky="w", padx=5)
        nomes_professores = [p.get_nome() for p in self.professores_cadastrados]
        self.cb_professor = ttk.Combobox(frame_topo, values=nomes_professores, state="readonly", font=("Segoe UI", 10))
        self.cb_professor.grid(row=1, column=3, sticky="ew", padx=5, pady=(2, 5))

        # PAINEL CENTRAL: LISTA DE CHAMADA COM TREEVIEW
        frame_centro = tk.Frame(self, bg="#E6CCB6")
        frame_centro.pack(fill="both", expand=True, padx=25, pady=8)

        # Barra de atalhos rápidos
        frame_botoes_rapidos = tk.Frame(frame_centro, bg="#E6CCB6")
        frame_botoes_rapidos.pack(fill="x", pady=(0, 6))

        tk.Label(frame_botoes_rapidos, text="Lista de Alunos da Turma:", font=("Segoe UI", 11, "bold"), bg="#E6CCB6").pack(side="left")

        btn_todos_presentes = tk.Button(frame_botoes_rapidos, text="✔ Todos Presentes", command=self.marcar_todos_presentes, bg="#2E7D32", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT)
        btn_todos_presentes.pack(side="right", padx=5)

        btn_todos_faltas = tk.Button(frame_botoes_rapidos, text="✖ Todos Faltaram", command=self.marcar_todos_faltas, bg="#C62828", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT)
        btn_todos_faltas.pack(side="right", padx=5)

        btn_alternar = tk.Button(frame_botoes_rapidos, text="🔄 Alternar Selecionado", command=self.alternar_presenca_selecionada, bg="#D2A27F", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT)
        btn_alternar.pack(side="right", padx=5)

        # Tabela Treeview
        colunas = ("id", "matricula", "nome", "status")
        self.tabela = ttk.Treeview(frame_centro, columns=colunas, show="headings", height=10)
        self.tabela.heading("id", text="ID")
        self.tabela.heading("matricula", text="Matrícula")
        self.tabela.heading("nome", text="Nome do Aluno")
        self.tabela.heading("status", text="Situação de Presença")

        self.tabela.column("id", width=60, minwidth=50, anchor="center")
        self.tabela.column("matricula", width=100, minwidth=80, anchor="center")
        self.tabela.column("nome", width=320, minwidth=200, anchor="w")
        self.tabela.column("status", width=160, minwidth=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_centro, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        self.tabela.bind("<Double-1>", lambda e: self.alternar_presenca_selecionada())
        self.tabela.bind("<space>", lambda e: self.alternar_presenca_selecionada())

        # PAINEL INFERIOR: BOTÕES DE SALVAR E NAVEGAÇÃO
        frame_inferior = tk.Frame(self, bg="#E6CCB6")
        frame_inferior.pack(pady=12)

        btn_salvar = tk.Button(
            frame_inferior,
            text="💾 Salvar Frequência",
            command=self.salvar_frequencia,
            bg="#B06C4B",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            width=20,
            height=1
        )
        btn_salvar.grid(row=0, column=0, padx=8)

        btn_historico = tk.Button(
            frame_inferior,
            text="📋 Ver Histórico de Chamadas",
            command=self.abrir_historico,
            bg="#6A3A2A",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            width=24,
            height=1
        )
        btn_historico.grid(row=0, column=1, padx=8)

        btn_voltar = tk.Button(
            frame_inferior,
            text="← Voltar ao Menu",
            command=master.mostrar_menu,
            bg="#D2A27F",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            width=16,
            height=1
        )
        btn_voltar.grid(row=0, column=2, padx=8)

        # Seleciona a primeira turma se disponível
        if self.nomes_turmas:
            self.cb_turma.current(0)
            self.ao_selecionar_turma()

    def obter_turma_selecionada(self):
        indice = self.cb_turma.current()
        if indice >= 0 and indice < len(self.turmas_carregadas):
            return self.turmas_carregadas[indice]
        return None

    def ao_selecionar_turma(self, event=None):
        turma = self.obter_turma_selecionada()
        if not turma:
            return

        # Preenche o professor regente da turma se existir
        if turma.professor:
            for idx, p in enumerate(self.professores_cadastrados):
                if p.get_nome() == turma.professor:
                    self.cb_professor.current(idx)
                    break

        if turma.disciplina:
            self.txt_disciplina.delete(0, tk.END)
            self.txt_disciplina.insert(0, turma.disciplina)

        # Carrega os alunos da turma selecionada
        self.alunos_chamada.clear()
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for nome_aluno in turma.alunos:
            aluno_obj = self.mapa_alunos.get(nome_aluno)
            aluno_id = aluno_obj.id if aluno_obj else None
            matricula = aluno_obj.matricula if aluno_obj else ""

            self.alunos_chamada.append({
                "id": aluno_id,
                "matricula": matricula,
                "nome": nome_aluno,
                "presente": True
            })

        self.atualizar_visualizacao_tabela()

    def atualizar_visualizacao_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for idx, item in enumerate(self.alunos_chamada):
            status_texto = "✔ Presente" if item["presente"] else "✖ Falta"
            self.tabela.insert(
                "",
                "end",
                iid=str(idx),
                values=(item["id"] or "-", item["matricula"] or "-", item["nome"], status_texto)
            )

    def alternar_presenca_selecionada(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        for item_id in selecionados:
            try:
                idx = int(item_id)
                self.alunos_chamada[idx]["presente"] = not self.alunos_chamada[idx]["presente"]
            except (ValueError, IndexError):
                continue

        self.atualizar_visualizacao_tabela()
        # Restaura a seleção
        for item_id in selecionados:
            if self.tabela.exists(item_id):
                self.tabela.selection_add(item_id)

    def marcar_todos_presentes(self):
        for item in self.alunos_chamada:
            item["presente"] = True
        self.atualizar_visualizacao_tabela()

    def marcar_todos_faltas(self):
        for item in self.alunos_chamada:
            item["presente"] = False
        self.atualizar_visualizacao_tabela()

    def salvar_frequencia(self):
        turma = self.obter_turma_selecionada()
        if not turma:
            messagebox.showwarning("Aviso", "Selecione uma turma válida.")
            return

        nome_prof = self.cb_professor.get().strip()
        prof_obj = next((p for p in self.professores_cadastrados if p.get_nome() == nome_prof), None)
        prof_id = prof_obj.id if prof_obj else turma.professor_id

        if not prof_id:
            messagebox.showwarning("Aviso", "Selecione um professor cadastrado para assinar a chamada.")
            return

        data_chamada = self.txt_data.get().strip()
        disciplina = self.txt_disciplina.get().strip() or "Regência"

        registros = []
        for a in self.alunos_chamada:
            if not a["id"]:
                # Tenta buscar pelo nome se o ID não estiver no cache
                aluno_obj = self.mapa_alunos.get(a["nome"])
                if aluno_obj:
                    a["id"] = aluno_obj.id

            if a["id"]:
                registros.append({
                    "aluno_id": a["id"],
                    "presente": a["presente"],
                    "aluno_nome": a["nome"]
                })

        if not registros:
            messagebox.showwarning("Aviso", "Nenhum aluno válido para registrar frequência.")
            return

        try:
            total_salvos = self.registrar_frequencia_uc.executar(
                turma_id=turma.id,
                professor_id=prof_id,
                disciplina=disciplina,
                data_chamada=data_chamada,
                registros=registros
            )
            messagebox.showinfo(
                "Sucesso",
                f"Frequência registrada com sucesso para {total_salvos} aluno(s) em {data_chamada}!"
            )
        except ValidationError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def abrir_historico(self):
        """Abre uma janela secundária exibindo os registros de frequência anteriores."""
        janela_hist = tk.Toplevel(self)
        janela_hist.title("Histórico de Frequências")
        janela_hist.geometry("800x450")
        janela_hist.configure(bg="#E6CCB6")

        tk.Label(janela_hist, text="Histórico Geral de Frequências", font=("Segoe UI", 14, "bold"), bg="#E6CCB6").pack(pady=10)

        colunas = ("data", "turma", "disciplina", "professor", "aluno", "status")
        tabela_hist = ttk.Treeview(janela_hist, columns=colunas, show="headings")
        tabela_hist.heading("data", text="Data")
        tabela_hist.heading("turma", text="Turma")
        tabela_hist.heading("disciplina", text="Disciplina")
        tabela_hist.heading("professor", text="Professor")
        tabela_hist.heading("aluno", text="Aluno")
        tabela_hist.heading("status", text="Situação")

        tabela_hist.column("data", width=90, anchor="center")
        tabela_hist.column("turma", width=120, anchor="center")
        tabela_hist.column("disciplina", width=100, anchor="center")
        tabela_hist.column("professor", width=130, anchor="w")
        tabela_hist.column("aluno", width=150, anchor="w")
        tabela_hist.column("status", width=90, anchor="center")

        scroll = ttk.Scrollbar(janela_hist, orient="vertical", command=tabela_hist.yview)
        tabela_hist.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tabela_hist.pack(fill="both", expand=True, padx=15, pady=10)

        try:
            registros = self.listar_frequencias_uc.executar()
            if not registros:
                messagebox.showinfo("Histórico", "Nenhum registro de frequência encontrado.")
            for r in registros:
                sit = "✔ Presente" if r.presente else "✖ Falta"
                tabela_hist.insert("", "end", values=(
                    r.data,
                    r.turma_nome or f"Turma {r.turma_id}",
                    r.disciplina,
                    r.professor_nome or f"Prof {r.professor_id}",
                    r.aluno_nome or f"Aluno {r.aluno_id}",
                    sit
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar histórico: {e}")

