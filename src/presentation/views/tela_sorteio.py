import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from src.domain.exceptions import ValidationError


class TelaSorteio(tk.Frame): # classe 6
    def __init__(self, master):
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.sortear_turmas_uc = master.sortear_turmas_uc
        self.listar_professores_uc = master.listar_professores_uc

        tk.Label(self, text="Sorteador de Turmas", font=("Segoe UI", 16, "bold"), bg="#E6CCB6").pack(pady=10)

        frame_config = tk.Frame(self, bg="#E6CCB6")
        frame_config.pack(pady=10, padx=20, fill="x")

        frame_config.columnconfigure(0, weight=1)
        frame_config.columnconfigure(1, weight=1)
        frame_config.columnconfigure(2, weight=1)
        frame_config.columnconfigure(3, weight=1)

        # 1. Série
        bloco_serie = tk.Frame(frame_config, bg="#E6CCB6")
        bloco_serie.grid(row=0, column=0, sticky="n", padx=10)

        tk.Label(bloco_serie, text="1. Escolha a Série:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").pack(anchor="w", pady=2)
        self.cb_serie_sorteio = ttk.Combobox(bloco_serie, values=self.master.series_predefinidas, state="readonly", width=15)
        self.cb_serie_sorteio.pack(fill="x", pady=5)
        self.cb_serie_sorteio.current(0)

        # 2. Quantidade de Turmas e Ano Letivo
        bloco_params = tk.Frame(frame_config, bg="#E6CCB6")
        bloco_params.grid(row=0, column=1, sticky="n", padx=10)

        tk.Label(bloco_params, text="2. Dividir em quantas turmas?", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").pack(anchor="w", pady=2)
        self.txt_qtd_turmas = tk.Entry(bloco_params, width=8, font=("Segoe UI", 10))
        self.txt_qtd_turmas.insert(0, "2")
        self.txt_qtd_turmas.pack(anchor="w", pady=5)

        tk.Label(bloco_params, text="Ano Letivo:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").pack(anchor="w", pady=(8, 2))
        self.txt_ano_letivo = tk.Entry(bloco_params, width=8, font=("Segoe UI", 10))
        self.txt_ano_letivo.insert(0, str(datetime.date.today().year))
        self.txt_ano_letivo.pack(anchor="w", pady=5)

        # 3. Professores
        bloco_prof = tk.Frame(frame_config, bg="#E6CCB6")
        bloco_prof.grid(row=0, column=2, sticky="n", padx=10)

        tk.Label(bloco_prof, text="3. Professores Disponíveis:", font=("Segoe UI", 10, "bold"), bg="#E6CCB6").pack(anchor="w", pady=2)

        self.listbox_professores = tk.Listbox(bloco_prof, selectmode="multiple", height=5, width=28, font=("Segoe UI", 9))
        self.listbox_professores.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(bloco_prof, orient="vertical", command=self.listbox_professores.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_professores.config(yscrollcommand=scrollbar.set)

        professores_cadastrados = self.listar_professores_uc.executar()
        nomes_professores = [prof.get_nome() for prof in professores_cadastrados]
        if not nomes_professores:
            self.listbox_professores.insert(tk.END, "Nenhum professor cadastrado")
            self.listbox_professores.config(state="disabled")
        else:
            for nome in nomes_professores:
                self.listbox_professores.insert(tk.END, nome)

        # 4. Botão de ação
        bloco_botao = tk.Frame(frame_config, bg="#E6CCB6")
        bloco_botao.grid(row=0, column=3, padx=10, sticky="s")

        btn_sortear = tk.Button(
            bloco_botao,
            text="Realizar Sorteio",
            command=self.realizar_sorteio,
            bg="#B06C4B",
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=8
        )
        btn_sortear.pack()

        self.txt_resultado = tk.Text(self, width=60, height=14, font=("Segoe UI", 10), relief=tk.SOLID, borderwidth=1)
        self.txt_resultado.pack(pady=10, padx=20, fill="both", expand=True)

        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=("Segoe UI", 10), command=master.mostrar_menu, bg="#D2A27F", fg="white", relief=tk.FLAT)
        btn_voltar.pack(pady=10)

    def realizar_sorteio(self):
        serie_alvo = self.cb_serie_sorteio.get()

        try:
            num_turmas = int(self.txt_qtd_turmas.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido de turmas.")
            return

        try:
            ano_letivo = int(self.txt_ano_letivo.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira um ano letivo válido.")
            return

        indices_selecionados = self.listbox_professores.curselection()
        professores_selecionados = [self.listbox_professores.get(i) for i in indices_selecionados]

        try:
            turmas_criadas = self.sortear_turmas_uc.executar(
                serie_alvo=serie_alvo,
                num_turmas=num_turmas,
                professores_selecionados=professores_selecionados,
                ano_letivo=ano_letivo
            )
        except ValidationError as e:
            messagebox.showwarning("Aviso", str(e))
            return
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        turmas_validas = [t for t in turmas_criadas if len(t.alunos) >= 1]
        total_alunos = sum(len(t.alunos) for t in turmas_validas)

        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, f"RESULTADO DO SORTEIO DE TURMAS: {serie_alvo.upper()} (Ano Letivo {ano_letivo})\n")
        self.txt_resultado.insert(tk.END, f"Total de alunos alocados: {total_alunos}\n")
        self.txt_resultado.insert(tk.END, "\n" + "=" * 60 + "\n\n")

        for turma in turmas_validas:
            self.txt_resultado.insert(tk.END, f"📌 {turma.nome} ({len(turma.alunos)} alunos) | Ano: {turma.ano_letivo}\n")
            self.txt_resultado.insert(tk.END, f"  Professor regente: {turma.professor} (Disciplina: {turma.disciplina})\n")
            self.txt_resultado.insert(tk.END, f"  Integrantes:\n")

            for aluno in turma.alunos:
                self.txt_resultado.insert(tk.END, f"  - {aluno}\n")
            self.txt_resultado.insert(tk.END, "\n" + "-" * 40 + "\n\n")
