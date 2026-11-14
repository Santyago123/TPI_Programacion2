from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from consola import crear_menu
from enums import Rol
from excepciones import CredencialesInvalidasError

def main() -> None:
    categorias=CategoriaServicio(); productos=ProductoServicio()
    usuarios=UsuarioServicio(); pedidos=PedidoServicio()
    usuarios.crear(nombre="Santiago",apellido="Lucero",mail="admin@foodstore.com",
                   celular="2610000000",contrasenia="admin123",rol=Rol.ADMIN)
    usuarios.crear(nombre="Martín",apellido="González", mail="martin@gmail.com", celular="2614567890", contrasenia="martin123", rol=Rol.USUARIO
)
    print("=== FOOD STORE ===")
    while True:
        usuario=None
        for intento in range(1,4):
            try:
                mail=input("Mail: "); contrasenia=input("Contraseña: ")
                usuario=usuarios.autenticar(mail,contrasenia); break
            except CredencialesInvalidasError as e:
                print(e)
                if intento==3:
                    print("Se agotaron los 3 intentos. Fin del programa.")
                    return
        if usuario:
            print(f"Bienvenido/a, {usuario.nombre} [{usuario.rol.value}]")
            menu=crear_menu(usuario,categorias,productos,usuarios,pedidos)
            if not menu.mostrar(): return

if __name__ == "__main__":
    main()

