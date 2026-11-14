from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, StockInsuficienteError

class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario is None or usuario.eliminado: raise DatoInvalidoError("Usuario inválido")
        self.__usuario = usuario
        self.__fecha = date.today()
        self.__estado = Estado.PENDIENTE
        self.__total = 0.0
        self.__forma_pago = forma_pago
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario: return self.__usuario
    @property
    def fecha(self) -> date: return self.__fecha
    @property
    def estado(self) -> Estado: return self.__estado
    @property
    def total(self) -> float: return self.__total
    @property
    def forma_pago(self) -> FormaPago: return self.__forma_pago
    @forma_pago.setter
    def forma_pago(self, v: FormaPago) -> None: self.__forma_pago = v
    @property
    def detalles(self) -> tuple[DetallePedido, ...]: return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if producto is None or producto.eliminado or not producto.disponible:
            raise DatoInvalidoError("Producto no disponible")
        if cantidad <= 0: raise DatoInvalidoError("Cantidad inválida")
        existente = self.buscar_detalle_por_producto(producto)
        total_solicitado = cantidad + (existente.cantidad if existente else 0)
        if total_solicitado > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}")
        if existente: existente.sumar_cantidad(cantidad)
        else: self.__detalles.append(DetallePedido(cantidad, producto, producto.precio))
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        return next((d for d in self.__detalles if d.producto == producto), None)

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle: self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(d.subtotal for d in self.__detalles)

    def cambiar_estado(self, nuevo: Estado) -> None:
        validos = {
            Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
            Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO),
        }
        if nuevo not in validos.get(self.__estado, ()):
            raise DatoInvalidoError("Transición de estado inválida")
        self.__estado = nuevo

    def __str__(self) -> str:
        return f"[{self.id}] {self.usuario.nombre} | {self.estado.value} | {self.forma_pago.value} | ${self.total:.2f} | {self.fecha}"
