from abc import ABC, abstractmethod
from src.domain.entities.turma import Turma


class TurmaRepository(ABC):
    """Contrato (Interface) para persistência e recuperação de Turmas."""

    @abstractmethod
    def salvar_todas(self, turmas: list[Turma]) -> None:
        pass

    @abstractmethod
    def listar_todas(self) -> list[Turma]:
        pass

    @abstractmethod
    def limpar(self) -> None:
        pass

