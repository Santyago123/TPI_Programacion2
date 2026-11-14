# Food Store — Sistema de Gestión de Pedidos de Comida

Aplicación de consola desarrollada en **Python 3.12 o superior** para administrar un negocio de comidas. El proyecto aplica Programación Orientada a Objetos (POO), separación por capas, colecciones en memoria, validaciones y excepciones propias.

## Contenido del repositorio

```text
food_store/
├── main.py
├── consola.py
├── servicios.py
├── enums.py
├── excepciones.py
├── pruebas.py
├── README.md
└── entidades/
    ├── __init__.py
    ├── base.py
    ├── calculable.py
    ├── categoria.py
    ├── producto.py
    ├── usuario.py
    ├── pedido.py
    └── detalle_pedido.py
```

## Organización por capas

- **Entidades (`entidades/`):** clases del dominio, atributos, propiedades y comportamientos.
- **Servicios (`servicios.py`):** administración de colecciones y reglas de negocio.
- **Consola (`consola.py`):** interacción mediante menús para administrador y cliente.
- **Enumerados (`enums.py`):** roles, estados de pedidos y formas de pago.
- **Excepciones (`excepciones.py`):** errores propios del sistema.
- **Punto de entrada (`main.py`):** inicialización de servicios, datos iniciales y autenticación.
- **Pruebas (`pruebas.py`):** pruebas manuales de operaciones y errores.

## Requisitos

- Python **3.12 o superior**.
- No requiere instalar paquetes externos: utiliza la biblioteca estándar de Python.

Comprobar la versión instalada:

```bash
python --version
```

## Cómo ejecutar

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

2. Entrar en la carpeta del proyecto:

```bash
cd food_store
```

3. Ejecutar la aplicación:

```bash
python main.py
```

En algunos sistemas puede ser necesario utilizar `python3 main.py`.

## Credenciales iniciales

El sistema crea un administrador inicial al arrancar:

| Campo | Credencial |
|---|---|
| Correo | `admin@foodstore.com` |
| Contraseña | `admin123` |
| Rol | `ADMIN` |

Para probar el rol cliente, se puede crear un usuario desde el menú de administración. Si se agrega un cliente de ejemplo en `main.py`, incorporar sus credenciales aquí.

> **Importante:** son credenciales de demostración. No utilizar contraseñas reales ni reutilizadas.

## Ejecutar las pruebas

Desde la carpeta raíz:

```bash
python pruebas.py
```

Verificar antes de la entrega que las pruebas cubran los casos de uso y las reglas de negocio solicitadas.

## Documentación y presentación

Completar estos datos antes de entregar:

- **Video de presentación:** `PEGAR_AQUI_EL_ENLACE_PUBLICO_DEL_VIDEO`
- **Informe PDF:** [Informe del proyecto](./informe/Food_Store_Informe.pdf)

Crear la carpeta `informe/` en la raíz y colocar allí el PDF con el nombre `Food_Store_Informe.pdf`. También se puede subir el PDF directamente a la raíz y actualizar el enlace.

El video debe tener permisos de visualización para cualquier persona que disponga del enlace.

## Almacenamiento

Los datos se guardan en colecciones en memoria mientras el programa está en ejecución. No se utiliza una base de datos ni persistencia en archivos. Al cerrar la aplicación, los datos cargados se pierden, tal como establece la consigna.

## Tecnologías y conceptos aplicados

- Python 3.12+
- Programación Orientada a Objetos
- Clases abstractas e interfaz mediante `abc`
- Herencia y polimorfismo
- Encapsulamiento mediante atributos privados y `@property`
- Enumeraciones con `enum`
- Fechas con `datetime`
- Colecciones (`list`)
- Excepciones propias, validaciones y type hints

## Autor

- **Estudiante:** COMPLETAR CON NOMBRE Y APELLIDO
- **Materia:** Programación II
- **Proyecto:** Trabajo Práctico Integrador — Food Store
