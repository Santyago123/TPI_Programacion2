from entidades.categoria import Categoria
from entidades.producto import Producto
from entidades.usuario import Usuario
from entidades.pedido import Pedido
from enums import Estado, FormaPago
from excepciones import *

class ServicioBase:
    def __init__(self) -> None: self._items: list = []
    def listar(self) -> list: return [x for x in self._items if not x.eliminado]
    def buscar(self, ident: int):
        for x in self._items:
            if x.id == ident and not x.eliminado: return x
        raise EntidadNoEncontradaError("Entidad inexistente o eliminada")
    def eliminar(self, ident: int) -> None: self.buscar(ident).eliminar()

class CategoriaServicio(ServicioBase):
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.lower() == nombre.strip().lower() and not c.eliminado for c in self._items):
            raise DuplicadoError("Ya existe una categoría con ese nombre")
        c = Categoria(nombre, descripcion); self._items.append(c); return c
    def editar(self, ident: int, nombre: str | None, descripcion: str | None) -> Categoria:
        c = self.buscar(ident)
        nuevo = nombre.strip() if nombre and nombre.strip() else c.nombre
        if nuevo.lower() != c.nombre.lower() and any(x.nombre.lower()==nuevo.lower() and not x.eliminado for x in self._items):
            raise DuplicadoError("Nombre de categoría repetido")
        c.nombre = nuevo
        if descripcion and descripcion.strip(): c.descripcion = descripcion
        return c
    def eliminar(self, ident: int, productos: list[Producto]) -> None:
        c = self.buscar(ident)
        activos = [p for p in productos if not p.eliminado and p.categoria == c]
        if activos: raise OperacionNoPermitidaError(f"La categoría tiene {len(activos)} productos activos")
        c.eliminar()

class ProductoServicio(ServicioBase):
    def crear(self, **datos) -> Producto:
        p = Producto(**datos); self._items.append(p); return p
    def editar(self, ident: int, **datos) -> Producto:
        p = self.buscar(ident)
        for k,v in datos.items():
            if v is not None and v != "": setattr(p,k,v)
        return p

class UsuarioServicio(ServicioBase):
    def crear(self, **datos) -> Usuario:
        mail = datos["mail"].lower()
        if any(u.mail == mail for u in self._items): raise DuplicadoError("El mail ya existe")
        u = Usuario(**datos); self._items.append(u); return u
    def editar(self, ident: int, **datos) -> Usuario:
        u = self.buscar(ident)
        mail = datos.pop("mail", None)
        if mail and mail.lower() != u.mail and any(x.mail == mail.lower() for x in self._items):
            raise DuplicadoError("El mail ya existe")
        if mail: u.mail = mail
        for k,v in datos.items():
            if v is not None and v != "": setattr(u,k,v)
        return u
    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for u in self._items:
            if u.mail == mail.strip().lower() and not u.eliminado and u.verificar_contrasenia(contrasenia):
                return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")
    def eliminar(self, ident: int, sesion: Usuario) -> None:
        u = self.buscar(ident)
        if u == sesion: raise OperacionNoPermitidaError("No puedes eliminarte a ti mismo")
        u.eliminar()

class PedidoServicio(ServicioBase):
    def crear(self, usuario: Usuario, forma_pago: FormaPago, detalles: list[tuple[Producto,int]]) -> Pedido:
        pedido = Pedido(usuario, forma_pago)
        # Primero valida todo; así no se modifica stock si falla.
        for producto,cantidad in detalles: pedido.agregar_detalle(cantidad, producto)
        if not pedido.detalles: raise DatoInvalidoError("El pedido debe tener al menos un detalle")
        for producto,cantidad in detalles: producto.stock -= cantidad
        self._items.append(pedido); return pedido
    def cambiar_estado(self, ident: int, nuevo: Estado) -> Pedido:
        p = self.buscar(ident)
        if nuevo == Estado.CANCELADO and p.estado != Estado.CANCELADO:
            for d in p.detalles: d.producto.stock += d.cantidad
        p.cambiar_estado(nuevo); return p
    def eliminar(self, ident: int) -> None:
        p = self.buscar(ident)
        if p.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for d in p.detalles: d.producto.stock += d.cantidad
        for d in p.detalles: d.eliminar()
        p.eliminar()
