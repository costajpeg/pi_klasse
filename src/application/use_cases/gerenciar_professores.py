from src.application.interfaces.professor_repository import ProfessorRepository
from src.domain.entities.professor import Professor
from src.domain.exceptions import ValidationError


class CadastrarProfessorUseCase:
    """Caso de uso para registrar um novo professor no sistema conforme as tabelas do banco."""
    def __init__(self, professor_repo: ProfessorRepository):
        self.professor_repo = professor_repo

    def executar(
        self,
        nome: str,
        matricula: str,
        email: str,
        cpf: str = ""
    ) -> Professor:
        nome_limpo = (nome or "").strip()
        matricula_limpa = (matricula or "").strip()
        email_limpo = (email or "").strip()
        cpf_limpo = (cpf or "").strip()

        if not nome_limpo:
            raise ValidationError("Por favor, preencha o nome do professor.")

        novo_id = self.professor_repo.proximo_id()

        # Garante valores válidos para as colunas NOT NULL e UNIQUE do banco
        if not matricula_limpa:
            matricula_limpa = f"PRF{novo_id:04d}"
        if not email_limpo:
            email_limpo = f"prof{novo_id}@escola.com"
        if not cpf_limpo:
            cpf_limpo = f"111.{novo_id:03d}.111-00"

        professor = Professor(
            nome=nome_limpo,
            matricula=matricula_limpa,
            email=email_limpo,
            cpf=cpf_limpo,
            id=novo_id
        )
        return self.professor_repo.salvar(professor)


class ListarProfessoresUseCase:
    """Caso de uso para listar todos os professores cadastrados."""
    def __init__(self, professor_repo: ProfessorRepository):
        self.professor_repo = professor_repo

    def executar(self) -> list[Professor]:
        return self.professor_repo.listar_todos()
