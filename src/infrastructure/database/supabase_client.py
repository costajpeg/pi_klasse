import os
from dotenv import load_dotenv
from supabase import create_client, Client
from src.domain.exceptions import DatabaseError

# Carrega variáveis do arquivo .env localizado na raiz do projeto
load_dotenv()

_client: Client | None = None


def get_supabase_client() -> Client | None:
    """Retorna uma instância única (Singleton) do cliente Supabase ou None caso não esteja configurado."""
    global _client
    if _client is not None:
        return _client

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()

    # Valida se as variáveis foram preenchidas e não são os valores de exemplo
    if not url or not key or "seu-projeto" in url or "sua-chave" in key:
        return None

    try:
        _client = create_client(url, key)
        return _client
    except Exception as e:
        print(f"[Supabase] Erro ao inicializar cliente Supabase: {e}")
        return None


def is_supabase_configured() -> bool:
    """Verifica se as variáveis de ambiente necessárias para o Supabase foram preenchidas."""
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    return bool(url and key and "seu-projeto" not in url and "sua-chave" not in key)


def formatar_erro_supabase(e: Exception) -> DatabaseError:
    """Traduz erros do Supabase/PostgREST para mensagens didáticas e fáceis de resolver."""
    msg = str(e)
    # Erro de Row Level Security (RLS) bloqueando INSERT/UPDATE/DELETE
    if "42501" in msg or "row-level security" in msg.lower():
        return DatabaseError(
            "Permissão negada pelo Supabase (Row Level Security - RLS ativo)!\n\n"
            "Para resolver:\n"
            "Vá no SQL Editor do painel do Supabase e execute os comandos para desativar o RLS:\n\n"
            "ALTER TABLE public.professores DISABLE ROW LEVEL SECURITY;\n"
            "ALTER TABLE public.alunos DISABLE ROW LEVEL SECURITY;\n"
            "ALTER TABLE public.turmas DISABLE ROW LEVEL SECURITY;\n"
            "ALTER TABLE public.turma_professores DISABLE ROW LEVEL SECURITY;\n"
            "ALTER TABLE public.historico_alunos_turmas DISABLE ROW LEVEL SECURITY;"
        )
    # Violação de UNIQUE (ex: matrícula repetida, cpf repetido, e-mail repetido)
    if "23505" in msg or "unique" in msg.lower():
        return DatabaseError(
            "Registro duplicado! Já existe um registro com essa mesma Matrícula, CPF ou E-mail cadastrado."
        )
    return DatabaseError(f"Erro na operação do banco de dados: {msg}")
