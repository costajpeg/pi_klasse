class DomainError(Exception):
    """Exceção base para erros na camada de domínio."""
    pass


class ValidationError(DomainError):
    """Lançada quando uma regra de validação de dados é violada."""
    pass


class DatabaseError(Exception):
    """Lançada quando ocorre uma falha de comunicação ou permissão no banco de dados."""
    pass
