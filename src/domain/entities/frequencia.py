class Frequencia:
    """Entidade que representa o registro de frequência/chamada de um aluno."""
    def __init__(
        self,
        turma_id: int,
        professor_id: int,
        aluno_id: int,
        disciplina: str,
        data: str,
        presente: bool = True,
        id: int | None = None,
        aluno_nome: str = "",
        turma_nome: str = "",
        professor_nome: str = ""
    ):
        self.id = id
        self.turma_id = turma_id
        self.professor_id = professor_id
        self.aluno_id = aluno_id
        self.disciplina = disciplina
        self.data = data
        self.presente = presente
        self.aluno_nome = aluno_nome
        self.turma_nome = turma_nome
        self.professor_nome = professor_nome

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "turma_id": self.turma_id,
            "professor_id": self.professor_id,
            "aluno_id": self.aluno_id,
            "disciplina": self.disciplina,
            "data": self.data,
            "presente": self.presente
        }

