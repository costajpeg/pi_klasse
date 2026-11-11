from src.application.interfaces.frequencia_repository import FrequenciaRepository
from src.domain.entities.frequencia import Frequencia


class InMemoryFrequenciaRepository(FrequenciaRepository):
    """Implementação em memória do repositório de frequências."""
    def __init__(self):
        self._frequencias: list[Frequencia] = []

    def salvar_lote(self, frequencias: list[Frequencia]) -> None:
        for f in frequencias:
            if f.id is None:
                f.id = len(self._frequencias) + 1
            # Se já existir registro para a mesma turma, data e aluno, atualiza
            existente = None
            for item in self._frequencias:
                if (item.turma_id == f.turma_id and
                    item.aluno_id == f.aluno_id and
                    item.data == f.data):
                    existente = item
                    break

            if existente:
                existente.presente = f.presente
                existente.disciplina = f.disciplina
                existente.professor_id = f.professor_id
            else:
                self._frequencias.append(f)

    def listar_por_turma_e_data(self, turma_id: int, data: str) -> list[Frequencia]:
        return [
            f for f in self._frequencias
            if f.turma_id == turma_id and f.data == data
        ]

    def listar_todas(self) -> list[Frequencia]:
        return list(self._frequencias)

