from abc import ABC, abstractmethod
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma


class HistoricoRepository(ABC):
    """Contrato (Interface) para persistência e recuperação do histórico de alunos em turmas."""

    @abstractmethod
    def salvar(self, historico: HistoricoAlunoTurma) -> HistoricoAlunoTurma:
        pass

    @abstractmethod
    def listar_todos(self) -> list[HistoricoAlunoTurma]:
        pass

    @abstractmethod
    def listar_por_aluno(self, aluno_id: int) -> list[HistoricoAlunoTurma]:
        pass

    @abstractmethod
    def listar_por_turma(self, turma_id: int) -> list[HistoricoAlunoTurma]:
        pass

    @abstractmethod
    def listar_por_ano_letivo(self, ano_letivo: int) -> list[HistoricoAlunoTurma]:
        pass

