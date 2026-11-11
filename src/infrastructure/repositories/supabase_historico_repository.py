from supabase import Client
from src.application.interfaces.historico_repository import HistoricoRepository
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma
from src.infrastructure.database.supabase_client import formatar_erro_supabase


class SupabaseHistoricoRepository(HistoricoRepository):
    """Implementação do repositório persistindo na tabela public.historico_alunos_turmas do Supabase."""
    def __init__(self, client: Client):
        self.client = client
        self.tabela = "historico_alunos_turmas"

    def salvar(self, historico: HistoricoAlunoTurma) -> HistoricoAlunoTurma:
        dados = {
            "aluno_id": historico.aluno_id,
            "turma_id": historico.turma_id,
            "ano_letivo": historico.ano_letivo,
            "serie": historico.serie
        }
        try:
            res = self.client.table(self.tabela).insert(dados).execute()
            if res.data and len(res.data) > 0:
                historico.id = res.data[0].get("id")
            return historico
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_todos(self) -> list[HistoricoAlunoTurma]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome, matricula), turmas(nome)")
                .order("ano_letivo", desc=True)
                .order("id", desc=True)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_por_aluno(self, aluno_id: int) -> list[HistoricoAlunoTurma]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome, matricula), turmas(nome)")
                .eq("aluno_id", aluno_id)
                .order("ano_letivo", desc=True)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_por_turma(self, turma_id: int) -> list[HistoricoAlunoTurma]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome, matricula), turmas(nome)")
                .eq("turma_id", turma_id)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def listar_por_ano_letivo(self, ano_letivo: int) -> list[HistoricoAlunoTurma]:
        try:
            res = (
                self.client.table(self.tabela)
                .select("*, alunos(nome, matricula), turmas(nome)")
                .eq("ano_letivo", ano_letivo)
                .execute()
            )
            return self._mapear_registros(res.data or [])
        except Exception as e:
            raise formatar_erro_supabase(e)

    def _mapear_registros(self, linhas: list[dict]) -> list[HistoricoAlunoTurma]:
        resultado = []
        for r in linhas:
            nome_aluno = ""
            mat_aluno = ""
            dados_aluno = r.get("alunos")
            if isinstance(dados_aluno, dict):
                nome_aluno = dados_aluno.get("nome", "")
                mat_aluno = dados_aluno.get("matricula", "")
            elif isinstance(dados_aluno, list) and len(dados_aluno) > 0:
                nome_aluno = dados_aluno[0].get("nome", "")
                mat_aluno = dados_aluno[0].get("matricula", "")

            nome_turma = ""
            dados_turma = r.get("turmas")
            if isinstance(dados_turma, dict):
                nome_turma = dados_turma.get("nome", "")
            elif isinstance(dados_turma, list) and len(dados_turma) > 0:
                nome_turma = dados_turma[0].get("nome", "")

            hist = HistoricoAlunoTurma(
                id=r.get("id"),
                aluno_id=r["aluno_id"],
                turma_id=r["turma_id"],
                ano_letivo=r["ano_letivo"],
                serie=r["serie"],
                aluno_nome=nome_aluno,
                aluno_matricula=mat_aluno,
                turma_nome=nome_turma
            )
            resultado.append(hist)
        return resultado

