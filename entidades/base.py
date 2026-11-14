from abc import ABC
from datetime import datetime

class Base(ABC):
    _contador: int = 1

    def __init__(self) -> None:
        self.__id: int = Base._contador
        Base._contador += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int: return self.__id
    @property
    def eliminado(self) -> bool: return self.__eliminado
    @property
    def creado_en(self) -> datetime: return self.__creado_en

    def eliminar(self) -> None:
        self.__eliminado = True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Base) and self.id == other.id
