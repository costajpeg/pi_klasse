from src.domain.entities.pessoa import Pessoa


class Professor(Pessoa): # classe com herança
    def __init__(
        self,
        nome: str,
        matricula: str,
        email: str = "",
        cpf: str = "",
        id: int | None = None
    ):
        super().__init__(nome=nome, cpf=cpf)
        self.matricula = matricula
        self.email = email
        self.id = id

    def mostrar_dados(self, extra: str | None = None) -> str: # polimorfismo mesmo metodo parametros diferentes
        # simula sobrecarga usando parametro opcional
        detalhes = f"Professor: {self.get_nome()} | Matrícula: {self.matricula}"
        if self.email:
            detalhes += f" | E-mail: {self.email}"
        if extra: # verifica se foi passada uma informação "extra"
            return f"{detalhes} | {extra}"
        return detalhes
