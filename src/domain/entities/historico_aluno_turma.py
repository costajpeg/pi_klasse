class HistoricoAlunoTurma:
    """Entidade que representa o registro histórico da vinculação de um aluno a uma turma em determinado ano letivo."""
    def __init__(
        self,
        aluno_id: int,
        turma_id: int,
        ano_letivo: int,
        serie: str,
        id: int | None = None,
        aluno_nome: str = "",
        aluno_matricula: str = "",
        turma_nome: str = ""
    ):
        self.id = id
        self.aluno_id = aluno_id
        self.turma_id = turma_id
        self.ano_letivo = ano_letivo
        self.serie = serie
        self.aluno_nome = aluno_nome
        self.aluno_matricula = aluno_matricula
        self.turma_nome = turma_nome

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "turma_id": self.turma_id,
            "ano_letivo": self.ano_letivo,
            "serie": self.serie
        }

