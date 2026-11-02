import random
import datetime
from src.application.interfaces.aluno_repository import AlunoRepository
from src.application.interfaces.professor_repository import ProfessorRepository
from src.application.interfaces.turma_repository import TurmaRepository
from src.application.interfaces.historico_repository import HistoricoRepository
from src.domain.entities.turma import Turma
from src.domain.entities.historico_aluno_turma import HistoricoAlunoTurma
from src.domain.exceptions import ValidationError


class SortearTurmasUseCase:
    """Caso de uso responsável pela divisão e sorteio de turmas conforme o modelo relacional."""
    def __init__(
        self,
        aluno_repo: AlunoRepository,
        turma_repo: TurmaRepository,
        professor_repo: ProfessorRepository | None = None,
        historico_repo: HistoricoRepository | None = None
    ):
        self.aluno_repo = aluno_repo
        self.turma_repo = turma_repo
        self.professor_repo = professor_repo
        self.historico_repo = historico_repo

    def executar(
        self,
        serie_alvo: str,
        num_turmas: int,
        professores_selecionados: list[str],
        ano_letivo: int | None = None
    ) -> list[Turma]:
        if num_turmas <= 0:
            raise ValidationError("O número de turmas deve ser maior que 0.")

        profs_validos = [p for p in professores_selecionados if p and p != "Nenhum professor cadastrado"]
        if not profs_validos:
            raise ValidationError("Por favor, selecione ao menos um professor para o sorteio.")

        alunos = self.aluno_repo.listar_por_serie(serie_alvo)
        nomes_alunos = [aluno.get_nome() for aluno in alunos]

        if not nomes_alunos:
            raise ValidationError(f"Não há alunos cadastrados no {serie_alvo}.")

        ano_atual = ano_letivo or datetime.date.today().year

        alunos_embaralhados = list(nomes_alunos)
        profs_embaralhados = list(profs_validos)
        random.shuffle(alunos_embaralhados)
        random.shuffle(profs_embaralhados)

        # Se houver mais turmas solicitadas do que alunos, ajusta para não criar turmas vazias
        qtd_turmas_efetivas = min(num_turmas, len(alunos_embaralhados))
        turmas_resultado: list[list[str]] = [[] for _ in range(qtd_turmas_efetivas)]

        for i, aluno_nome in enumerate(alunos_embaralhados):
            indice_turma = i % qtd_turmas_efetivas
            turmas_resultado[indice_turma].append(aluno_nome)

        letras_turmas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        novas_turmas: list[Turma] = []

        # Mapeia nomes de professores para seus objetos/IDs se o repositório estiver disponível
        mapa_professores = {}
        if self.professor_repo:
            for prof in self.professor_repo.listar_todos():
                mapa_professores[prof.get_nome()] = prof

        # Consulta turmas já existentes para manter o histórico e continuar a sequência de letras
        turmas_existentes = self.turma_repo.listar_todas()
        turmas_mesma_serie = [
            t for t in turmas_existentes
            if t.serie == serie_alvo and t.ano_letivo == ano_atual
        ]
        deslocamento_letras = len(turmas_mesma_serie)

        for idx, lista_alunos in enumerate(turmas_resultado):
            # Não cria turma com menos de um aluno
            if not lista_alunos or len(lista_alunos) < 1:
                continue

            letra = letras_turmas[(deslocamento_letras + idx) % 26]
            nome_turma = f"Turma {serie_alvo} {letra}"
            nome_prof = profs_embaralhados[idx % len(profs_embaralhados)]
            prof_obj = mapa_professores.get(nome_prof)
            prof_id = prof_obj.id if prof_obj else None

            turma = Turma(
                nome=nome_turma,
                serie=serie_alvo,
                ano_letivo=ano_atual,
                professor=nome_prof,
                professor_id=prof_id,
                disciplina="Regência",
                alunos=lista_alunos
            )
            novas_turmas.append(turma)

        self.turma_repo.salvar_todas(novas_turmas)

        # Atualiza o repositório de histórico (especialmente útil em modo InMemory)
        if self.historico_repo:
            mapa_alunos_obj = {a.get_nome(): a for a in self.aluno_repo.listar_todos()}
            for t in novas_turmas:
                for nome_a in t.alunos:
                    aluno_obj = mapa_alunos_obj.get(nome_a)
                    aluno_id = aluno_obj.id if aluno_obj else None
                    if aluno_id and t.id:
                        reg_hist = HistoricoAlunoTurma(
                            aluno_id=aluno_id,
                            turma_id=t.id,
                            ano_letivo=t.ano_letivo,
                            serie=t.serie,
                            aluno_nome=nome_a,
                            aluno_matricula=aluno_obj.matricula if aluno_obj else "",
                            turma_nome=t.nome
                        )
                        self.historico_repo.salvar(reg_hist)

        return novas_turmas


class ListarTurmasUseCase:
    """Caso de uso para consultar turmas cadastradas, com opção de ignorar turmas vazias."""
    def __init__(self, turma_repo: TurmaRepository):
        self.turma_repo = turma_repo

    def executar(self, apenas_com_alunos: bool = True) -> list[Turma]:
        turmas = self.turma_repo.listar_todas()
        if apenas_com_alunos:
            # Não retorna turmas com menos de um aluno
            return [t for t in turmas if len(t.alunos) >= 1]
        return turmas
