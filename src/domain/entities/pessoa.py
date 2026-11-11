from abc import ABC, abstractmethod # biblioteca abstrata


class Pessoa(ABC): # classe abstrata pois herda ABC
    def __init__(self, nome: str, cpf: str = ""):
        self.__nome = nome # atributo privado
        self.cpf = cpf

    @abstractmethod
    def mostrar_dados(self):
        """Método abstrato que deve ser implementado pelas subclasses."""
        pass

    def get_nome(self) -> str:
        return self.__nome # atributo privado

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def validar_nome(self) -> bool: # método de validação
        return bool(self.__nome and len(self.__nome.strip()) > 0)
