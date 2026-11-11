from src.infrastructure.repositories.in_memory_aluno_repository import InMemoryAlunoRepository
from src.infrastructure.repositories.in_memory_professor_repository import InMemoryProfessorRepository
from src.infrastructure.repositories.in_memory_turma_repository import InMemoryTurmaRepository
from src.infrastructure.repositories.in_memory_frequencia_repository import InMemoryFrequenciaRepository
from src.infrastructure.repositories.in_memory_historico_repository import InMemoryHistoricoRepository

from src.infrastructure.repositories.supabase_aluno_repository import SupabaseAlunoRepository
from src.infrastructure.repositories.supabase_professor_repository import SupabaseProfessorRepository
from src.infrastructure.repositories.supabase_turma_repository import SupabaseTurmaRepository
from src.infrastructure.repositories.supabase_frequencia_repository import SupabaseFrequenciaRepository
from src.infrastructure.repositories.supabase_historico_repository import SupabaseHistoricoRepository

__all__ = [
    "InMemoryAlunoRepository",
    "InMemoryProfessorRepository",
    "InMemoryTurmaRepository",
    "InMemoryFrequenciaRepository",
    "InMemoryHistoricoRepository",
    "SupabaseAlunoRepository",
    "SupabaseProfessorRepository",
    "SupabaseTurmaRepository",
    "SupabaseFrequenciaRepository",
    "SupabaseHistoricoRepository",
]
