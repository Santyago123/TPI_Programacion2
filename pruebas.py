from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from enums import Rol, FormaPago
from excepciones import FoodStoreError

cat=CategoriaServicio(); prod=ProductoServicio(); usr=UsuarioServicio(); ped=PedidoServicio()
try:
    c=cat.crear("Pizzas","Pizzas artesanales")
    p=prod.crear(nombre="Muzzarella",precio=5000.0,descripcion="Grande",stock=10,imagen="",disponible=True,categoria=c)
    u=usr.crear(nombre="Juan",apellido="Gomez",mail="juan@test.com",celular="123",contrasenia="1234",rol=Rol.USUARIO)
    pedido=ped.crear(u,FormaPago.EFECTIVO,[(p,2)])
    print("CASO VÁLIDO:",pedido)
    try: ped.crear(u,FormaPago.EFECTIVO,[(p,100)])
    except FoodStoreError as e: print("ERROR ESPERADO:",e)
    print("Stock final:",p.stock)
except FoodStoreError as e: print("Error:",e)
