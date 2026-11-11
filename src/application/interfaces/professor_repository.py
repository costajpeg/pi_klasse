from abc import ABC, abstractmethod
from src.domain.entities.professor import Professor


class ProfessorRepository(ABC):
    """Contrato (Interface) para persistência e recuperação de Professores."""

    @abstractmethod
    def salvar(self, professor: Professor) -> Professor:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Professor]:
        pass

    @abstractmethod
    def obter_por_nome(self, nome: str) -> Professor | None:
        pass

    @abstractmethod
    def proximo_id(self) -> int:
        pass
