import datetime


class Turma:
    """Entidade que representa uma turma escolar formada por série, ano letivo, professor e alunos."""
    def __init__(
        self,
        nome: str,
        serie: str,
        ano_letivo: int | None = None,
        professor: str = "",
        professor_id: int | None = None,
        disciplina: str = "Regência",
        alunos: list[str] | None = None,
        id: int | None = None
    ):
        self.id = id
        self.nome = nome
        self.serie = serie
        self.ano_letivo = ano_letivo if ano_letivo is not None else datetime.date.today().year
        self.professor = professor
        self.professor_id = professor_id
        self.disciplina = disciplina
        self.alunos = list(alunos) if alunos else []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "serie": self.serie,
            "ano_letivo": self.ano_letivo,
            "professor": self.professor,
            "professor_id": self.professor_id,
            "disciplina": self.disciplina,
            "alunos": self.alunos
        }
