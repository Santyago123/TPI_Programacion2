from entidades.base import Base
from entidades.producto import Producto
from excepciones import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto, precio_unitario: float) -> None:
        super().__init__()
        if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor a cero")
        self.__cantidad: int = cantidad
        self.__producto: Producto = producto
        self.__precio_unitario: float = precio_unitario
        self.__subtotal: float = cantidad * precio_unitario

    @property
    def cantidad(self) -> int: return self.__cantidad
    @property
    def producto(self) -> Producto: return self.__producto
    @property
    def subtotal(self) -> float: return self.__subtotal

    def sumar_cantidad(self, cantidad: int) -> None:
        if cantidad <= 0: raise DatoInvalidoError("Cantidad inválida")
        self.__cantidad += cantidad
        self.__subtotal = self.__cantidad * self.__precio_unitario

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal:.2f}"
