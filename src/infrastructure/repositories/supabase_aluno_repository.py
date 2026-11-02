from supabase import Client
from src.application.interfaces.aluno_repository import AlunoRepository
from src.domain.entities.aluno import Aluno
from src.infrastructure.database.supabase_client import formatar_erro_supabase


class SupabaseAlunoRepository(AlunoRepository):
    """Implementação do repositório de alunos persistindo na tabela public.alunos do Supabase."""
    def __init__(self, client: Client):
        self.client = client
        self.tabela = "alunos"

    def salvar(self, aluno: Aluno) -> Aluno:
        dados = {
            "nome": aluno.get_nome(),
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "data_nascimento": aluno.data_nascimento,
            "serie_atual": aluno.serie,
            "turma_atual_id": aluno.turma_atual_id
        }
        try:
            resposta = self.client.table(self.tabela).insert(dados).execute()
            if resposta.data and len(resposta.data) > 0:
                aluno.id = resposta.data[0].get("id")
            return aluno
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_todos(self) -> list[Aluno]:
        try:
            resposta = self.client.table(self.tabela).select("*").order("id").execute()
            return [
                Aluno(
                    nome=r["nome"],
                    serie=r["serie_atual"],
                    matricula=r.get("matricula", ""),
                    cpf=r.get("cpf", ""),
                    data_nascimento=str(r.get("data_nascimento", "")),
                    turma_atual_id=r.get("turma_atual_id"),
                    id=r.get("id")
                )
                for r in (resposta.data or [])
            ]
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_por_serie(self, serie: str) -> list[Aluno]:
        try:
            resposta = (
                self.client.table(self.tabela)
                .select("*")
                .eq("serie_atual", serie)
                .order("id")
                .execute()
            )
            return [
                Aluno(
                    nome=r["nome"],
                    serie=r["serie_atual"],
                    matricula=r.get("matricula", ""),
                    cpf=r.get("cpf", ""),
                    data_nascimento=str(r.get("data_nascimento", "")),
                    turma_atual_id=r.get("turma_atual_id"),
                    id=r.get("id")
                )
                for r in (resposta.data or [])
            ]
        except Exception as e:
            raise formatar_erro_supabase(e)

    def atualizar_turma(self, aluno_id: int, turma_id: int | None) -> None:
        try:
            self.client.table(self.tabela).update({"turma_atual_id": turma_id}).eq("id", aluno_id).execute()
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
