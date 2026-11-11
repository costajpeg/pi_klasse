from supabase import Client
from src.application.interfaces.turma_repository import TurmaRepository
from src.domain.entities.turma import Turma
from src.infrastructure.database.supabase_client import formatar_erro_supabase


class SupabaseTurmaRepository(TurmaRepository):
    """Implementação do repositório de turmas persistindo nas tabelas relacionais do Supabase."""
    def __init__(self, client: Client):
        self.client = client

    def salvar_todas(self, turmas: list[Turma]) -> None:
        try:
            if not turmas:
                return

            for t in turmas:
                # 1. Insere o registro na tabela turmas (mantendo as turmas já existentes no banco)
                dados_turma = {
                    "nome": t.nome,
                    "serie": t.serie,
                    "ano_letivo": t.ano_letivo
                }
                res_turma = self.client.table("turmas").insert(dados_turma).execute()
                if not res_turma.data:
                    continue

                turma_id = res_turma.data[0]["id"]
                t.id = turma_id

                # 2. Relaciona o professor regente na tabela turma_professores
                prof_id = t.professor_id
                if not prof_id and t.professor:
                    res_prof = self.client.table("professores").select("id").eq("nome", t.professor).limit(1).execute()
                    if res_prof.data:
                        prof_id = res_prof.data[0]["id"]

                if prof_id:
                    dados_tp = {
                        "turma_id": turma_id,
                        "professor_id": prof_id,
                        "disciplina": t.disciplina or "Regência"
                    }
                    self.client.table("turma_professores").insert(dados_tp).execute()

                # 3. Atualiza os alunos para pertencerem a esta turma e registra no histórico
                for aluno_nome in t.alunos:
                    res_aluno = self.client.table("alunos").select("id").eq("nome", aluno_nome).limit(1).execute()
                    if res_aluno.data:
                        aluno_id = res_aluno.data[0]["id"]
                        self.client.table("alunos").update({"turma_atual_id": turma_id}).eq("id", aluno_id).execute()
                        self.client.table("historico_alunos_turmas").insert({
                            "aluno_id": aluno_id,
                            "turma_id": turma_id,
                            "ano_letivo": t.ano_letivo,
                            "serie": t.serie
                        }).execute()
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_todas(self) -> list[Turma]:
        try:
            res_turmas = self.client.table("turmas").select("*").order("id").execute()
            turmas_resultado: list[Turma] = []

            for r_turma in (res_turmas.data or []):
                turma_id = r_turma["id"]

                prof_nome = ""
                prof_id = None
                disciplina = "Regência"

                res_tp = self.client.table("turma_professores").select("professor_id, disciplina, professores(nome)").eq("turma_id", turma_id).execute()
                if res_tp.data and len(res_tp.data) > 0:
                    item_tp = res_tp.data[0]
                    prof_id = item_tp.get("professor_id")
                    disciplina = item_tp.get("disciplina") or "Regência"
                    dados_prof = item_tp.get("professores")
                    if isinstance(dados_prof, dict):
                        prof_nome = dados_prof.get("nome", "")
                    elif isinstance(dados_prof, list) and len(dados_prof) > 0:
                        prof_nome = dados_prof[0].get("nome", "")

                res_alunos = self.client.table("alunos").select("nome").eq("turma_atual_id", turma_id).order("nome").execute()
                alunos_nomes = [a["nome"] for a in (res_alunos.data or [])]

                turma_obj = Turma(
                    id=turma_id,
                    nome=r_turma["nome"],
                    serie=r_turma["serie"],
                    ano_letivo=r_turma["ano_letivo"],
                    professor=prof_nome,
                    professor_id=prof_id,
                    disciplina=disciplina,
                    alunos=alunos_nomes
                )
                turmas_resultado.append(turma_obj)

            return turmas_resultado
        except Exception as e:
            raise formatar_erro_supabase(e)

    def limpar(self) -> None:
        try:
            self.client.table("alunos").update({"turma_atual_id": None}).neq("id", 0).execute()
            self.client.table("historico_alunos_turmas").delete().gte("id", 0).execute()
            self.client.table("turma_professores").delete().gte("id", 0).execute()
            self.client.table("turmas").delete().gte("id", 0).execute()
        except Exception as e:
            raise formatar_erro_supabase(e)
