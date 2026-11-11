
from abc import ABC, abstractmethod
from src.domain.entities.aluno import Aluno


class AlunoRepository(ABC):
    """Contrato para persistência e recuperação de alunos."""

    @abstractmethod
    def salvar(self, aluno: Aluno) -> Aluno:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Aluno]:
        pass

    @abstractmethod
    def buscar_por_id(self, aluno_id: int) -> Aluno | None:
        pass

    @abstractmethod
    def listar_por_serie(self, serie: str) -> list[Aluno]:
        pass

    @abstractmethod
    def atualizar_turma(self, aluno_id: int, turma_id: int | None) -> None:
        pass

    @abstractmethod
    def proximo_id(self) -> int:
        pass
