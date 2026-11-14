from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):
    def __init__(self, nombre: str, precio: float, descripcion: str, stock: int,
                 imagen: str, disponible: bool, categoria: Categoria) -> None:
        super().__init__()
        self.nombre = nombre; self.precio = precio; self.descripcion = descripcion
        self.stock = stock; self.imagen = imagen; self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v or not v.strip(): raise DatoInvalidoError("Nombre inválido")
        self.__nombre = v.strip()

    @property
    def precio(self) -> float: return self.__precio
    @precio.setter
    def precio(self, v: float) -> None:
        if v < 0: raise PrecioInvalidoError("El precio no puede ser negativo")
        self.__precio = float(v)

    @property
    def descripcion(self) -> str: return self.__descripcion
    @descripcion.setter
    def descripcion(self, v: str) -> None:
        if not v or not v.strip(): raise DatoInvalidoError("Descripción inválida")
        self.__descripcion = v.strip()

    @property
    def stock(self) -> int: return self.__stock
    @stock.setter
    def stock(self, v: int) -> None:
        if v < 0: raise DatoInvalidoError("El stock no puede ser negativo")
        self.__stock = int(v)

    @property
    def imagen(self) -> str: return self.__imagen
    @imagen.setter
    def imagen(self, v: str) -> None: self.__imagen = v.strip()

    @property
    def disponible(self) -> bool: return self.__disponible
    @disponible.setter
    def disponible(self, v: bool) -> None: self.__disponible = bool(v)

    @property
    def categoria(self) -> Categoria: return self.__categoria
    @categoria.setter
    def categoria(self, v: Categoria) -> None:
        if v is None or v.eliminado: raise DatoInvalidoError("Categoría inválida")
        self.__categoria = v

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} | ${self.precio:.2f} | Stock: {self.stock} | {self.categoria.nombre}"
