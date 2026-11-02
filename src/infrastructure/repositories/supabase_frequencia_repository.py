from supabase import Client
from src.application.interfaces.frequencia_repository import FrequenciaRepository
from src.domain.entities.frequencia import Frequencia
from src.infrastructure.database.supabase_client import formatar_erro_supabase


class SupabaseFrequenciaRepository(FrequenciaRepository):
    """Implementação do repositório de frequências persistindo na tabela public.frequencias do Supabase."""
    def __init__(self, client: Client):
        self.client = client
        self.tabela = "frequencias"

    def salvar_lote(self, frequencias: list[Frequencia]) -> None:
        try:
            if not frequencias:
                return

            dados = [
                {
                    "turma_id": f.turma_id,
                    "professor_id": f.professor_id,
                    "aluno_id": f.aluno_id,
                    "disciplina": f.disciplina,
                    "data": f.data,
                    "presente": f.presente
                }
                for f in frequencias
            ]

            # Remove registros prévios do mesmo dia/turma para evitar duplicidade de chamada
            turma_id = frequencias[0].turma_id
            data = frequencias[0].data
            self.client.table(self.tabela).delete().eq("turma_id", turma_id).eq("data", data).execute()

            # Insere os novos registros de frequência
            self.client.table(self.tabela).insert(dados).execute()
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_por_turma_e_data(self, turma_id: int, data: str) -> list[Frequencia]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome), professores(nome), turmas(nome)")
                .eq("turma_id", turma_id)
                .eq("data", data)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_todas(self) -> list[Frequencia]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome), professores(nome), turmas(nome)")
                .order("id", desc=True)
                .limit(200)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def _mapear_registros(self, linhas: list[dict]) -> list[Frequencia]:
        resultado = []
        for r in linhas:
            nome_aluno = ""
            if isinstance(r.get("alunos"), dict):
                nome_aluno = r["alunos"].get("nome", "")

            nome_prof = ""
            if isinstance(r.get("professores"), dict):
                nome_prof = r["professores"].get("nome", "")

            nome_turma = ""
            if isinstance(r.get("turmas"), dict):
                nome_turma = r["turmas"].get("nome", "")

            freq = Frequencia(
                id=r.get("id"),
                turma_id=r["turma_id"],
                professor_id=r["professor_id"],
                aluno_id=r["aluno_id"],
                disciplina=r["disciplina"],
                data=str(r["data"]),
                presente=bool(r.get("presente", True)),
                aluno_nome=nome_aluno,
                turma_nome=nome_turma,
                professor_nome=nome_prof
            )
            resultado.append(freq)
        return resultado

