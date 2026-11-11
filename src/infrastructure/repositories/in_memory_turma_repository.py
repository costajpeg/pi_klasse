from src.application.interfaces.turma_repository import TurmaRepository
from src.domain.entities.turma import Turma


class InMemoryTurmaRepository(TurmaRepository):
    """Implementação em memória do repositório de turmas."""
    def __init__(self):
        self._turmas: list[Turma] = []

    def salvar_todas(self, turmas: list[Turma]) -> None:
        for t in turmas:
            if t.id is None:
                t.id = len(self._turmas) + 1
            self._turmas.append(t)

    def listar_todas(self) -> list[Turma]:
        return list(self._turmas)

    def limpar(self) -> None:
        self._turmas.clear()

