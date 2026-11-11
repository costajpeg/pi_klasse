
from src.application.interfaces.aluno_repository import AlunoRepository
from src.domain.entities.aluno import Aluno


class InMemoryAlunoRepository(AlunoRepository):
    """Implementação em memória do repositório de alunos."""

    def __init__(self):
        self._alunos: list[Aluno] = []

    def salvar(self, aluno: Aluno) -> Aluno:
        if aluno.id is None:
            aluno.id = self.proximo_id()
        self._alunos.append(aluno)
        return aluno

    def listar_todos(self) -> list[Aluno]:
        return list(self._alunos)

    def buscar_por_id(self, aluno_id: int) -> Aluno | None:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def listar_por_serie(self, serie: str) -> list[Aluno]:
        return [
            aluno for aluno in self._alunos
            if aluno.serie == serie
        ]

    def atualizar_turma(self, aluno_id: int, turma_id: int | None) -> None:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                aluno.turma_atual_id = turma_id
                break

    def proximo_id(self) -> int:
        return len(self._alunos) + 1
