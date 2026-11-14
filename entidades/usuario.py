from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError

class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str,
                 contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre; self.apellido = apellido; self.mail = mail
        self.celular = celular; self.contrasenia = contrasenia; self.rol = rol

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("Nombre vacío")
        self.__nombre = v.strip()

    @property
    def apellido(self) -> str: return self.__apellido
    @apellido.setter
    def apellido(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("Apellido vacío")
        self.__apellido = v.strip()

    @property
    def mail(self) -> str: return self.__mail
    @mail.setter
    def mail(self, v: str) -> None:
        if not v.strip() or "@" not in v or "." not in v: raise DatoInvalidoError("Mail inválido")
        self.__mail = v.strip().lower()

    @property
    def celular(self) -> str: return self.__celular
    @celular.setter
    def celular(self, v: str) -> None: self.__celular = v.strip()

    @property
    def rol(self) -> Rol: return self.__rol
    @rol.setter
    def rol(self, v: Rol) -> None:
        if not isinstance(v, Rol): raise DatoInvalidoError("Rol inválido")
        self.__rol = v

    @property
    def contrasenia(self):
        raise AttributeError("La contraseña no puede leerse")

    @contrasenia.setter
    def contrasenia(self, v: str) -> None:
        if not v: raise DatoInvalidoError("Contraseña vacía")
        self.__contrasenia = v

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} {self.apellido} | {self.mail} | {self.rol.value}"
