from src.application.use_cases.gerenciar_alunos import (
    CadastrarAlunoUseCase,
    ListarAlunosUseCase,
    ListarAlunosPorSerieUseCase,
)
from src.application.use_cases.gerenciar_professores import (
    CadastrarProfessorUseCase,
    ListarProfessoresUseCase,
)
from src.application.use_cases.sortear_turmas import (
    SortearTurmasUseCase,
    ListarTurmasUseCase,
)
from src.application.use_cases.gerenciar_frequencias import (
    RegistrarFrequenciaUseCase,
    ListarFrequenciasUseCase,
)
from src.application.use_cases.gerenciar_historico import (
    RegistrarHistoricoUseCase,
    ListarHistoricoUseCase,
)

__all__ = [
    "CadastrarAlunoUseCase",
    "ListarAlunosUseCase",
    "ListarAlunosPorSerieUseCase",
    "CadastrarProfessorUseCase",
    "ListarProfessoresUseCase",
    "SortearTurmasUseCase",
    "ListarTurmasUseCase",
    "RegistrarFrequenciaUseCase",
    "ListarFrequenciasUseCase",
    "RegistrarHistoricoUseCase",
    "ListarHistoricoUseCase",
]
