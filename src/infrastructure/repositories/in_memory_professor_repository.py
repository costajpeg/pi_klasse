from src.application.interfaces.professor_repository import ProfessorRepository
from src.domain.entities.professor import Professor


class InMemoryProfessorRepository(ProfessorRepository):
    """Implementação em memória do repositório de professores."""
    def __init__(self):
        self._professores: list[Professor] = []

    def salvar(self, professor: Professor) -> Professor:
        if professor.id is None:
            professor.id = self.proximo_id()
        self._professores.append(professor)
        return professor

    def listar_todos(self) -> list[Professor]:
        return list(self._professores)

    def obter_por_nome(self, nome: str) -> Professor | None:
        for p in self._professores:
            if p.get_nome() == nome:
                return p
        return None

    def proximo_id(self) -> int:
        return len(self._professores) + 1
