from src.domain.entities.pessoa import Pessoa


class Aluno(Pessoa): # classe com herança
    def __init__(
        self,
        nome: str,
        serie: str,
        matricula: str = "",
        cpf: str = "",
        data_nascimento: str = "2015-01-01",
        turma_atual_id: int | None = None,
        id: int | None = None
    ):
        super().__init__(nome=nome, cpf=cpf)
        self.serie = serie # mapeia para serie_atual no banco de dados
        self.matricula = matricula
        self.data_nascimento = data_nascimento
        self.turma_atual_id = turma_atual_id
        self.id = id

    @property
    def serie_atual(self) -> str:
        return self.serie

    @serie_atual.setter
    def serie_atual(self, valor: str) -> None:
        self.serie = valor

    def mostrar_dados(self, extra: str | None = None) -> str: # polimorfismo mesmo metodo parametros diferentes
        # simula sobrecarga usando parametro opcional
        detalhes = f"Aluno: {self.get_nome()} | Série: {self.serie}"
        if self.matricula:
            detalhes += f" | Matrícula: {self.matricula}"
        if extra: # verifica se foi passada uma informação "extra"
            return f"{detalhes} | {extra}"
        return detalhes
