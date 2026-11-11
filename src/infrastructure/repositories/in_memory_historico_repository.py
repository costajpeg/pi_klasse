from src.application.interfaces.historico_repository import HistoricoRepository
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma


class InMemoryHistoricoRepository(HistoricoRepository):
    """Implementação em memória do repositório de histórico de alunos e turmas."""
    def __init__(self):
        self._historicos: list[HistoricoAlunoTurma] = []

    def salvar(self, historico: HistoricoAlunoTurma) -> HistoricoAlunoTurma:
        if historico.id is None:
            historico.id = len(self._historicos) + 1
        self._historicos.append(historico)
        return historico

    def listar_todos(self) -> list[HistoricoAlunoTurma]:
        return list(self._historicos)

    def listar_por_aluno(self, aluno_id: int) -> list[HistoricoAlunoTurma]:
        return [h for h in self._historicos if h.aluno_id == aluno_id]

    def listar_por_turma(self, turma_id: int) -> list[HistoricoAlunoTurma]:
        return [h for h in self._historicos if h.turma_id == turma_id]

    def listar_por_ano_letivo(self, ano_letivo: int) -> list[HistoricoAlunoTurma]:
        return [h for h in self._historicos if h.ano_letivo == ano_letivo]

