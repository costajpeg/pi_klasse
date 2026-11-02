from abc import ABC, abstractmethod
from src.domain.entities.frequencia import Frequencia


class FrequenciaRepository(ABC):
    """Contrato (Interface) para persistência e recuperação de Frequências escolares."""

    @abstractmethod
    def salvar_lote(self, frequencias: list[Frequencia]) -> None:
        pass

    @abstractmethod
    def listar_por_turma_e_data(self, turma_id: int, data: str) -> list[Frequencia]:
        pass

    @abstractmethod
    def listar_todas(self) -> list[Frequencia]:
        pass

