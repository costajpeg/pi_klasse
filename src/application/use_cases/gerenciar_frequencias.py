from src.application.interfaces.frequencia_repository import FrequenciaRepository
from src.application.use_cases.gerenciar_alunos import normalizar_data
from src.domain.entities.frequencia import Frequencia
from src.domain.exceptions import ValidationError


class RegistrarFrequenciaUseCase:
    """Caso de uso para registrar a chamada/frequência de uma turma em uma data."""
    def __init__(self, frequencia_repo: FrequenciaRepository):
        self.frequencia_repo = frequencia_repo

    def executar(
        self,
        turma_id: int,
        professor_id: int,
        disciplina: str,
        data_chamada: str,
        registros: list[dict]
    ) -> int:
        if not turma_id:
            raise ValidationError("Selecione uma turma válida para registrar a frequência.")

        if not professor_id:
            raise ValidationError("Selecione ou vincule um professor à turma.")

        disciplina_limpa = (disciplina or "").strip()
        if not disciplina_limpa:
            disciplina_limpa = "Regência"

        data_formatada = normalizar_data(data_chamada)
        if not data_formatada:
            raise ValidationError("Informe uma data válida para a chamada.")

        if not registros:
            raise ValidationError("Nenhum aluno informado para registrar presença.")

        lista_frequencias: list[Frequencia] = []
        for reg in registros:
            aluno_id = reg.get("aluno_id")
            if not aluno_id:
                continue

            freq = Frequencia(
                turma_id=turma_id,
                professor_id=professor_id,
                aluno_id=aluno_id,
                disciplina=disciplina_limpa,
                data=data_formatada,
                presente=bool(reg.get("presente", True)),
                aluno_nome=reg.get("aluno_nome", "")
            )
            lista_frequencias.append(freq)

        self.frequencia_repo.salvar_lote(lista_frequencias)
        return len(lista_frequencias)


class ListarFrequenciasUseCase:
    """Caso de uso para consultar o histórico de frequências registradas."""
    def __init__(self, frequencia_repo: FrequenciaRepository):
        self.frequencia_repo = frequencia_repo

    def executar(self, turma_id: int | None = None, data_chamada: str | None = None) -> list[Frequencia]:
        if turma_id and data_chamada:
            dt = normalizar_data(data_chamada)
            return self.frequencia_repo.listar_por_turma_e_data(turma_id, dt)
        return self.frequencia_repo.listar_todas()

