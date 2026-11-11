
import tkinter as tk
from tkinter import messagebox

from src.presentation.components.botao_personalizado import BotaoPersonalizado
from src.presentation.components.tela_base import TelaBase
from src.presentation.views.tela_alunos import TelaCadastroAlunos
from src.presentation.views.tela_perfil_aluno import TelaPerfilAluno
from src.presentation.views.tela_professores import TelaCadastroProfessores
from src.presentation.views.tela_sorteio import TelaSorteio
from src.presentation.views.tela_turmas import TelaTurmas
from src.presentation.views.tela_frequencia import TelaFrequencia
from src.presentation.views.tela_historico import TelaHistoricoAlunosTurmas


class Aplicativo(tk.Tk):
    def __init__(
        self,
        cadastrar_aluno_uc,
        listar_alunos_uc,
        cadastrar_professor_uc,
        listar_professores_uc,
        sortear_turmas_uc,
        listar_turmas_uc,
        registrar_frequencia_uc=None,
        listar_frequencias_uc=None,
        listar_historico_uc=None,
        registrar_historico_uc=None
    ):
        super().__init__()

        self.title("KLASSE")
        self.geometry("1000x740")
        self.configure(bg="#E6CCB6")

        self.cadastrar_aluno_uc = cadastrar_aluno_uc
        self.listar_alunos_uc = listar_alunos_uc
        self.cadastrar_professor_uc = cadastrar_professor_uc
        self.listar_professores_uc = listar_professores_uc
        self.sortear_turmas_uc = sortear_turmas_uc
        self.listar_turmas_uc = listar_turmas_uc
        self.registrar_frequencia_uc = registrar_frequencia_uc
        self.listar_frequencias_uc = listar_frequencias_uc
        self.listar_historico_uc = listar_historico_uc
        self.registrar_historico_uc = registrar_historico_uc

        self.series_predefinidas = [
            "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano",
            "6º Ano", "7º Ano", "8º Ano", "9º Ano"
        ]

        self.tela_atual = None
        self.mostrar_menu()

    def mostrar_menu(self):
        if self.tela_atual:
            self.tela_atual.destroy()

        self.tela_atual = tk.Frame(self, bg="#E6CCB6")
        self.tela_atual.pack(fill="both", expand=True)

        for i in range(7):
            self.tela_atual.rowconfigure(i, weight=1)

        self.tela_atual.columnconfigure(0, weight=1)

        botoes = [
            ("Professores", "Cadastro de Professores"),
            ("Alunos", "Cadastro de Alunos"),
            ("Turmas", "Turmas cadastradas"),
            ("Sortear Turmas", "Sorteio de Turmas"),
            ("Frequência", "Frequência dos Alunos"),
            ("Histórico Escolar", "Histórico de Turmas")
        ]

        for i, (texto, destino) in enumerate(botoes):
            botao = BotaoPersonalizado(
                self.tela_atual,
                text=texto,
                command=lambda d=destino: self.mudar_tela(d)
            )

            botao.grid(
                row=i,
                column=0,
                padx=2,
                pady=(50, 1) if i == 0 else 1
            )

        botao_sair = BotaoPersonalizado(
            self.tela_atual,
            text="Sair",
            command=self.destroy
        )

        botao_sair.grid(
            row=6,
            column=0,
            padx=2,
            pady=(1, 50)
        )

    def mudar_tela(self, titulo_nova_tela: str):
        if self.tela_atual:
            self.tela_atual.destroy()

        if titulo_nova_tela == "Cadastro de Professores":
            self.tela_atual = TelaCadastroProfessores(self)

        elif titulo_nova_tela == "Cadastro de Alunos":
            self.tela_atual = TelaCadastroAlunos(self)

        elif titulo_nova_tela == "Turmas cadastradas":
            self.tela_atual = TelaTurmas(self)

        elif titulo_nova_tela == "Sorteio de Turmas":
            self.tela_atual = TelaSorteio(self)

        elif titulo_nova_tela == "Frequência dos Alunos":
            self.tela_atual = TelaFrequencia(self)

        elif titulo_nova_tela == "Histórico de Turmas":
            self.tela_atual = TelaHistoricoAlunosTurmas(self)

        else:
            self.tela_atual = TelaBase(
                self,
                titulo_texto=titulo_nova_tela
            )

        self.tela_atual.pack(fill="both", expand=True)

    def abrir_perfil_aluno(self, aluno_id):
        try:
            alunos = self.listar_alunos_uc.executar()

            aluno = next(
                (a for a in alunos if a.id == aluno_id),
                None
            )

            if aluno is None:
                messagebox.showerror(
                    "Erro",
                    "Aluno não encontrado."
                )
                return

            if self.tela_atual:
                self.tela_atual.destroy()

            self.tela_atual = TelaPerfilAluno(self, aluno)
            self.tela_atual.pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir o perfil:\n{e}"
            )
