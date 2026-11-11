import tkinter as tk


class TelaTurmas(tk.Frame): # classe 7
    def __init__(self, master):
        super().__init__(master, bg="#E6CCB6")
        self.master = master
        self.listar_turmas_uc = master.listar_turmas_uc

        tk.Label(self, text="Turmas Cadastradas", font=("Segoe UI", 18, "bold"), bg="#E6CCB6").pack(pady=15)

        txt = tk.Text(self, font=("Segoe UI", 10))
        txt.pack(fill="both", expand=True, padx=20, pady=15)

        try:
            # Busca todas as turmas cadastradas, filtrando para não exibir turmas com menos de um aluno
            turmas = self.listar_turmas_uc.executar(apenas_com_alunos=True)
            turmas_com_alunos = [t for t in turmas if len(t.alunos) >= 1]

            if not turmas_com_alunos:
                txt.insert(tk.END, "Nenhuma turma com alunos cadastrada ou sorteada no banco ainda.\n")
            else:
                for turma in turmas_com_alunos:
                    txt.insert(tk.END, f"📌 {turma.nome} | Série: {turma.serie} | Ano Letivo: {turma.ano_letivo}\n")
                    if turma.professor:
                        txt.insert(tk.END, f"   Professor Regente: {turma.professor} ({turma.disciplina})\n")
                    txt.insert(tk.END, f"   Total de Alunos: {len(turma.alunos)}\n")
                    txt.insert(tk.END, "   Alunos:\n")

                    for aluno in turma.alunos:
                        txt.insert(tk.END, f"    - {aluno}\n")

                    txt.insert(tk.END, "\n" + "-" * 50 + "\n\n")
        except Exception as e:
            txt.insert(tk.END, f"Erro ao consultar turmas: {e}\n")

        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=("Segoe UI", 10), command=master.mostrar_menu, bg="#D2A27F", fg="white", relief=tk.FLAT)
        btn_voltar.pack(pady=10)
