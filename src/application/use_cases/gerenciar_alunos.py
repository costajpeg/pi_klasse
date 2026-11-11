import re
from src.application.interfaces.aluno_repository import AlunoRepository
from src.domain.entities.aluno import Aluno
from src.domain.exceptions import ValidationError


def normalizar_data(data_str: str) -> str:
    """Converte 'DD/MM/AAAA' para 'AAAA-MM-DD' caso necessário."""
    limpa = (data_str or "").strip()
    if not limpa:
        return "2015-01-01"
    if "/" in limpa:
        partes = limpa.split("/")
        if len(partes) == 3:
            d, m, a = partes
            return f"{a.strip():0>4}-{m.strip():0>2}-{d.strip():0>2}"
    return limpa


class CadastrarAlunoUseCase:
    """Caso de uso para registrar um novo aluno no sistema conforme as tabelas do banco."""
    def __init__(self, aluno_repo: AlunoRepository):
        self.aluno_repo = aluno_repo

    def executar(
        self,
        nome: str,
        serie: str,
        matricula: str = "",
        cpf: str = "",
        data_nascimento: str = ""
    ) -> Aluno:
        nome_limpo = (nome or "").strip()
        if not nome_limpo:
            raise ValidationError("Por favor, digite o nome do aluno.")

        serie_limpa = (serie or "").strip()
        if not serie_limpa:
            raise ValidationError("Por favor, selecione uma série válida.")

        novo_id = self.aluno_repo.proximo_id()

        # Garante valores válidos para restrições NOT NULL e UNIQUE do banco
        mat_limpa = (matricula or "").strip()
        if not mat_limpa:
            mat_limpa = f"ALU{novo_id:04d}"

        cpf_limpo = (cpf or "").strip()
        if not cpf_limpo:
            cpf_limpo = f"000.{novo_id:03d}.000-00"

        dt_nasc = normalizar_data(data_nascimento)

        aluno = Aluno(
            nome=nome_limpo,
            serie=serie_limpa,
            matricula=mat_limpa,
            cpf=cpf_limpo,
            data_nascimento=dt_nasc,
            id=novo_id
        )
        return self.aluno_repo.salvar(aluno)


class ListarAlunosUseCase:
    """Caso de uso para listar todos os alunos cadastrados."""
    def __init__(self, aluno_repo: AlunoRepository):
        self.aluno_repo = aluno_repo

    def executar(self) -> list[Aluno]:
        return self.aluno_repo.listar_todos()


class ListarAlunosPorSerieUseCase:
    """Caso de uso para listar alunos pertencentes a uma série específica."""
    def __init__(self, aluno_repo: AlunoRepository):
        self.aluno_repo = aluno_repo

    def executar(self, serie: str) -> list[Aluno]:
        return self.aluno_repo.listar_por_serie(serie)
