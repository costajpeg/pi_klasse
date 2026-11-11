import tkinter as tk
from src.presentation.components.botao_personalizado import BotaoPersonalizado
from src.presentation.components.tela_base import TelaBase
from src.presentation.views.tela_alunos import TelaCadastroAlunos
from src.presentation.views.tela_professores import TelaCadastroProfessores
from src.presentation.views.tela_sorteio import TelaSorteio
from src.presentation.views.tela_turmas import TelaTurmas
from src.presentation.views.tela_frequencia import TelaFrequencia
from src.presentation.views.tela_historico import TelaHistoricoAlunosTurmas


class Aplicativo(tk.Tk): # classe 3 tk.Tk eh a janela principal
    # superclasse
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

        # Injeção de dependência dos Casos de Uso (Clean Architecture)
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

        b1 = BotaoPersonalizado(self.tela_atual, text="Professores", command=lambda: self.mudar_tela("Cadastro de Professores"))
        b1.grid(row=0, column=0, sticky="", padx=2, pady=(50, 1))

        b2 = BotaoPersonalizado(self.tela_atual, text="Alunos", command=lambda: self.mudar_tela("Cadastro de Alunos"))
        b2.grid(row=1, column=0, sticky="", padx=2, pady=1)

        b3 = BotaoPersonalizado(self.tela_atual, text="Turmas", command=lambda: self.mudar_tela("Turmas cadastradas"))
        b3.grid(row=2, column=0, sticky="", padx=2, pady=1)

        b4 = BotaoPersonalizado(self.tela_atual, text="Sortear Turmas", command=lambda: self.mudar_tela("Sorteio de Turmas"))
        b4.grid(row=3, column=0, sticky="", padx=2, pady=1)

        b5 = BotaoPersonalizado(self.tela_atual, text="Frequência", command=lambda: self.mudar_tela("Frequência dos Alunos"))
        b5.grid(row=4, column=0, sticky="", padx=2, pady=1)

        b6 = BotaoPersonalizado(self.tela_atual, text="Histórico Escolar", command=lambda: self.mudar_tela("Histórico de Turmas"))
        b6.grid(row=5, column=0, sticky="", padx=2, pady=1)

        b7 = BotaoPersonalizado(self.tela_atual, text="Sair", command=self.destroy)
        b7.grid(row=6, column=0, sticky="", padx=2, pady=(1, 50))

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
            self.tela_atual = TelaBase(self, titulo_texto=titulo_nova_tela)

        self.tela_atual.pack(fill="both", expand=True)
