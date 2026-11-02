from supabase import Client
from src.application.interfaces.professor_repository import ProfessorRepository
from src.domain.entities.professor import Professor
from src.infrastructure.database.supabase_client import formatar_erro_supabase


class SupabaseProfessorRepository(ProfessorRepository):
    """Implementação do repositório de professores persistindo na tabela public.professores do Supabase."""
    def __init__(self, client: Client):
        self.client = client
        self.tabela = "professores"

    def salvar(self, professor: Professor) -> Professor:
        dados = {
            "nome": professor.get_nome(),
            "matricula": professor.matricula,
            "cpf": professor.cpf,
            "email": professor.email
        }
        try:
            resposta = self.client.table(self.tabela).insert(dados).execute()
            if resposta.data and len(resposta.data) > 0:
                professor.id = resposta.data[0].get("id")
            return professor
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_todos(self) -> list[Professor]:
        try:
            resposta = self.client.table(self.tabela).select("*").order("id").execute()
            return [
                Professor(
                    nome=r["nome"],
                    matricula=r["matricula"],
                    email=r.get("email", ""),
                    cpf=r.get("cpf", ""),
                    id=r.get("id")
                )
                for r in (resposta.data or [])
            ]
        except Exception as e:
            raise formatar_erro_supabase(e)

    def obter_por_nome(self, nome: str) -> Professor | None:
        try:
            resposta = self.client.table(self.tabela).select("*").eq("nome", nome).limit(1).execute()
            if resposta.data and len(resposta.data) > 0:
                r = resposta.data[0]
                return Professor(
                    nome=r["nome"],
                    matricula=r["matricula"],
                    email=r.get("email", ""),
                    cpf=r.get("cpf", ""),
                    id=r.get("id")
                )
            return None
        except Exception as e:
            raise formatar_erro_supabase(e)

    def proximo_id(self) -> int:
        try:
            resposta = (
                self.client.table(self.tabela)
                .select("id")
                .order("id", desc=True)
                .limit(1)
                .execute()
            )
            if resposta.data and len(resposta.data) > 0:
                return resposta.data[0]["id"] + 1
            return 1
        except Exception:
            return 1
