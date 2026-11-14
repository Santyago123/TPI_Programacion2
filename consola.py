from abc import ABC, abstractmethod
from enums import Rol, Estado, FormaPago
from excepciones import FoodStoreError

def entero(msg: str) -> int: return int(input(msg))
def flotante(msg: str) -> float: return float(input(msg))

def elegir_enum(enum_cls, titulo: str):
    valores = list(enum_cls)
    print(titulo)
    for i,v in enumerate(valores,1): print(f"{i}. {v.value}")
    n = entero("Seleccione: ")
    if not 1 <= n <= len(valores): raise ValueError("Opción fuera de rango")
    return valores[n-1]

class Menu(ABC):
    def __init__(self, usuario, categorias, productos, usuarios, pedidos) -> None:
        self.usuario=usuario; self.categorias=categorias; self.productos=productos
        self.usuarios=usuarios; self.pedidos=pedidos
    @abstractmethod
    def mostrar(self) -> bool: pass

    def listar(self, items) -> None:
        if not items: print("No hay datos cargados")
        for x in items: print(x)

class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - ADMINISTRADOR ({self.usuario.nombre}) ===")
            print("1. Categorías\n2. Productos\n3. Usuarios\n4. Pedidos\n9. Cerrar sesión\n0. Salir")
            try:
                op=input("Seleccione: ").strip()
                if op=="1": self.menu_categorias()
                elif op=="2": self.menu_productos()
                elif op=="3": self.menu_usuarios()
                elif op=="4": self.menu_pedidos()
                elif op=="9": return True
                elif op=="0": return False
                else: print("Opción inválida")
            except FoodStoreError as e: print("Error:",e)
            except ValueError as e: print("Dato inválido:",e)

    def menu_categorias(self):
        print("\n--- CATEGORÍAS ---\n1.Listar 2.Crear 3.Editar 4.Eliminar 0.Volver")
        op=input("Seleccione: ")
        if op=="1": self.listar(self.categorias.listar())
        elif op=="2":
            c=self.categorias.crear(input("Nombre: "),input("Descripción: ")); print(f"Creada con ID {c.id}")
        elif op=="3":
            self.listar(self.categorias.listar()); i=entero("ID: ")
            self.categorias.editar(i,input("Nuevo nombre (Enter conserva): "),input("Nueva descripción (Enter conserva): ")); print("Categoría actualizada")
        elif op=="4":
            self.listar(self.categorias.listar()); i=entero("ID: ")
            if input("Confirmar S/N: ").upper()=="S": self.categorias.eliminar(i,self.productos._items); print("Categoría eliminada")

    def menu_productos(self):
        print("\n--- PRODUCTOS ---\n1.Listar 2.Crear 3.Editar 4.Eliminar 0.Volver")
        op=input("Seleccione: ")
        if op=="1": self.listar(self.productos.listar())
        elif op=="2":
            self.listar(self.categorias.listar()); cat=self.categorias.buscar(entero("ID categoría: "))
            p=self.productos.crear(nombre=input("Nombre: "),precio=flotante("Precio: "),descripcion=input("Descripción: "),
                stock=entero("Stock: "),imagen=input("Imagen: "),disponible=input("Disponible S/N: ").upper()=="S",categoria=cat)
            print(f"Producto creado con ID {p.id}")
        elif op=="3":
            self.listar(self.productos.listar()); p=self.productos.buscar(entero("ID: "))
            precio=input(f"Precio [{p.precio}]: "); stock=input(f"Stock [{p.stock}]: ")
            nombre=input(f"Nombre [{p.nombre}]: "); descripcion=input(f"Descripción [{p.descripcion}]: ")
            self.productos.editar(p.id,nombre=nombre or None,descripcion=descripcion or None,
                precio=float(precio) if precio else None,stock=int(stock) if stock else None); print("Producto actualizado")
        elif op=="4":
            self.listar(self.productos.listar()); p=self.productos.buscar(entero("ID: "))
            if input("Confirmar S/N: ").upper()=="S": p.eliminar(); print("Producto eliminado")

    def menu_usuarios(self):
        print("\n--- USUARIOS ---\n1.Listar 2.Crear 3.Editar 4.Eliminar 0.Volver")
        op=input("Seleccione: ")
        if op=="1": self.listar(self.usuarios.listar())
        elif op=="2":
            rol=elegir_enum(Rol,"Rol")
            u=self.usuarios.crear(nombre=input("Nombre: "),apellido=input("Apellido: "),mail=input("Mail: "),
                celular=input("Celular: "),contrasenia=input("Contraseña: "),rol=rol); print(f"Usuario creado con ID {u.id}")
        elif op=="4":
            self.listar(self.usuarios.listar()); i=entero("ID: ")
            if input("Confirmar S/N: ").upper()=="S": self.usuarios.eliminar(i,self.usuario); print("Usuario eliminado")
        elif op=="3": print("Edición: puede implementarse con los mismos criterios de edición de categorías.")

    def menu_pedidos(self):
        print("\n--- PEDIDOS ---\n1.Listar 2.Crear 3.Cambiar estado/pago 4.Eliminar 0.Volver")
        op=input("Seleccione: ")
        if op=="1": self.listar(self.pedidos.listar())
        elif op=="2":
            self.listar(self.usuarios.listar()); usuario=self.usuarios.buscar(entero("ID usuario: "))
            pago=elegir_enum(FormaPago,"Forma de pago"); detalles=[]
            while True:
                self.listar(self.productos.listar()); pid=entero("ID producto (0 terminar): ")
                if pid==0: break
                detalles.append((self.productos.buscar(pid),entero("Cantidad: ")))
            p=self.pedidos.crear(usuario,pago,detalles); print(f"Pedido {p.id} creado. Total: ${p.total:.2f}")
        elif op=="3":
            p=self.pedidos.buscar(entero("ID pedido: "))
            estado=elegir_enum(Estado,"Nuevo estado")
            p=self.pedidos.cambiar_estado(p.id,estado)
            if input("¿Cambiar forma de pago? S/N: ").upper()=="S": p.forma_pago=elegir_enum(FormaPago,"Forma de pago")
            print("Pedido actualizado")
        elif op=="4":
            i=entero("ID pedido: ")
            if input("Confirmar S/N: ").upper()=="S": self.pedidos.eliminar(i); print("Pedido eliminado")

class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - CLIENTE ({self.usuario.nombre}) ===")
            print("1. Ver categorías\n2. Ver productos disponibles\n3. Mis pedidos\n4. Mis datos\n9. Cerrar sesión\n0. Salir")
            try:
                op=input("Seleccione: ")
                if op=="1": self.listar(self.categorias.listar())
                elif op=="2": self.listar([p for p in self.productos.listar() if p.disponible and p.stock>0])
                elif op=="3":
                    propios=[p for p in self.pedidos.listar() if p.usuario==self.usuario]; self.listar(propios)
                    if propios and input("¿Ver detalles? S/N: ").upper()=="S":
                        i=entero("ID pedido: "); p=next((x for x in propios if x.id==i),None)
                        if not p: print("Pedido inexistente")
                        else:
                            for d in p.detalles: print(" -",d)
                            print(f"Total: ${p.total:.2f}")
                elif op=="4": print(self.usuario)
                elif op=="9": return True
                elif op=="0": return False
                else: print("Opción inválida")
            except FoodStoreError as e: print("Error:",e)
            except ValueError as e: print("Dato inválido:",e)

def crear_menu(usuario, categorias, productos, usuarios, pedidos) -> Menu:
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario,categorias,productos,usuarios,pedidos)
    return MenuCliente(usuario,categorias,productos,usuarios,pedidos)
