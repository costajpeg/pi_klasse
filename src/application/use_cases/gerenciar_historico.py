from src.application.interfaces.historico_repository import HistoricoRepository
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma
from src.domain.exceptions import ValidationError


class RegistrarHistoricoUseCase:
    """Caso de uso para registrar a entrada de um aluno em uma turma no histórico."""
    def __init__(self, historico_repo: HistoricoRepository):
        self.historico_repo = historico_repo

    def executar(self, aluno_id: int, turma_id: int, ano_letivo: int, serie: str) -> HistoricoAlunoTurma:
        if not aluno_id:
            raise ValidationError("ID do aluno é obrigatório para registrar histórico.")
        if not turma_id:
            raise ValidationError("ID da turma é obrigatório para registrar histórico.")
        if not ano_letivo:
            raise ValidationError("Ano letivo é obrigatório para registrar histórico.")
        if not serie:
            raise ValidationError("Série é obrigatória para registrar histórico.")

        registro = HistoricoAlunoTurma(
            aluno_id=aluno_id,
            turma_id=turma_id,
            ano_letivo=ano_letivo,
            serie=serie.strip()
        )
        return self.historico_repo.salvar(registro)


class ListarHistoricoUseCase:
    """Caso de uso para consultar o histórico escolar com opções de filtro."""
    def __init__(self, historico_repo: HistoricoRepository):
        self.historico_repo = historico_repo

    def executar(
        self,
        aluno_id: int | None = None,
        turma_id: int | None = None,
        ano_letivo: int | None = None,
        serie: str | None = None
    ) -> list[HistoricoAlunoTurma]:
        registros = self.historico_repo.listar_todos()

        if aluno_id:
            registros = [r for r in registros if r.aluno_id == aluno_id]
        if turma_id:
            registros = [r for r in registros if r.turma_id == turma_id]
        if ano_letivo:
            registros = [r for r in registros if r.ano_letivo == ano_letivo]
        if serie and serie != "Todas":
            registros = [r for r in registros if r.serie == serie]

        return registros

