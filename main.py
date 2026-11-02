import sys
import os

# Adiciona a raiz do projeto ao sys.path para garantir importações consistentes
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importações de Domínio (Entidades e Regras de Negócio Centrais)
from src.domain.entities.pessoa import Pessoa # classe abstrata pois herda ABC
from src.domain.entities.aluno import Aluno # classe com herança
from src.domain.entities.professor import Professor # classe com herança
from src.domain.entities.turma import Turma
from src.domain.entities.frequencia import Frequencia
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma

# Importações de Infraestrutura (Conexão Supabase e Repositórios)
from src.infrastructure.database.supabase_client import get_supabase_client
from src.infrastructure.repositories import (
    InMemoryAlunoRepository,
    InMemoryProfessorRepository,
    InMemoryTurmaRepository,
    InMemoryFrequenciaRepository,
    InMemoryHistoricoRepository,
    SupabaseAlunoRepository,
    SupabaseProfessorRepository,
    SupabaseTurmaRepository,
    SupabaseFrequenciaRepository,
    SupabaseHistoricoRepository,
)

# Importações de Aplicação (Casos de Uso)
from src.application.use_cases import (
    CadastrarAlunoUseCase,
    ListarAlunosUseCase,
    ListarAlunosPorSerieUseCase,
    CadastrarProfessorUseCase,
    ListarProfessoresUseCase,
    SortearTurmasUseCase,
    ListarTurmasUseCase,
    RegistrarFrequenciaUseCase,
    ListarFrequenciasUseCase,
    RegistrarHistoricoUseCase,
    ListarHistoricoUseCase,
)

# Importações de Apresentação (Interface Gráfica)
from src.presentation.app import Aplicativo
from src.presentation.components.botao_personalizado import BotaoPersonalizado
from src.presentation.components.tela_base import TelaBase
from src.presentation.views.tela_alunos import TelaCadastroAlunos
from src.presentation.views.tela_professores import TelaCadastroProfessores
from src.presentation.views.tela_sorteio import TelaSorteio
from src.presentation.views.tela_turmas import TelaTurmas
from src.presentation.views.tela_frequencia import TelaFrequencia
from src.presentation.views.tela_historico import TelaHistoricoAlunosTurmas


def criar_aplicativo() -> Aplicativo:
    """Função de composição (Composition Root) que conecta as camadas da Clean Architecture."""
    # 1. Camada de Infraestrutura: Conexão e instanciação dos repositórios
    supabase = get_supabase_client()

    if supabase:
        print("[Banco de Dados] Conexao com Supabase ativada com sucesso! (Persistencia em Nuvem)")
        aluno_repo = SupabaseAlunoRepository(supabase)
        professor_repo = SupabaseProfessorRepository(supabase)
        turma_repo = SupabaseTurmaRepository(supabase)
        frequencia_repo = SupabaseFrequenciaRepository(supabase)
        historico_repo = SupabaseHistoricoRepository(supabase)
    else:
        print("[Banco de Dados] Supabase nao configurado no .env. Utilizando repositorio em memoria temporario.")
        print("[Dica] Para conectar ao Supabase, preencha o arquivo .env com SUPABASE_URL e SUPABASE_KEY.")
        aluno_repo = InMemoryAlunoRepository()
        professor_repo = InMemoryProfessorRepository()
        turma_repo = InMemoryTurmaRepository()
        frequencia_repo = InMemoryFrequenciaRepository()
        historico_repo = InMemoryHistoricoRepository()

    # 2. Camada de Aplicação: Instanciação dos Casos de Uso com injeção de dependências
    cadastrar_aluno_uc = CadastrarAlunoUseCase(aluno_repo)
    listar_alunos_uc = ListarAlunosUseCase(aluno_repo)
    cadastrar_professor_uc = CadastrarProfessorUseCase(professor_repo)
    listar_professores_uc = ListarProfessoresUseCase(professor_repo)
    sortear_turmas_uc = SortearTurmasUseCase(aluno_repo, turma_repo, professor_repo, historico_repo)
    listar_turmas_uc = ListarTurmasUseCase(turma_repo)
    registrar_frequencia_uc = RegistrarFrequenciaUseCase(frequencia_repo)
    listar_frequencias_uc = ListarFrequenciasUseCase(frequencia_repo)
    listar_historico_uc = ListarHistoricoUseCase(historico_repo)
    registrar_historico_uc = RegistrarHistoricoUseCase(historico_repo)

    # 3. Camada de Apresentação: Inicialização da interface gráfica Tkinter
    app = Aplicativo(
        cadastrar_aluno_uc=cadastrar_aluno_uc,
        listar_alunos_uc=listar_alunos_uc,
        cadastrar_professor_uc=cadastrar_professor_uc,
        listar_professores_uc=listar_professores_uc,
        sortear_turmas_uc=sortear_turmas_uc,
        listar_turmas_uc=listar_turmas_uc,
        registrar_frequencia_uc=registrar_frequencia_uc,
        listar_frequencias_uc=listar_frequencias_uc,
        listar_historico_uc=listar_historico_uc,
        registrar_historico_uc=registrar_historico_uc
    )
    return app


if __name__ == "__main__":
    # Testes didáticos demonstrando conceitos de Orientação a Objetos (POO):
    aluno_teste = Aluno("Alice", "5º Ano")
    professor_teste = Professor("Antônio", "12345")

    print(aluno_teste.mostrar_dados("Aluno destaque")) # chamada de método
    print(professor_teste.mostrar_dados("Professor homenageado")) # chamada de método

    app = criar_aplicativo()
    app.mainloop() # janela aberta e executa a interface
