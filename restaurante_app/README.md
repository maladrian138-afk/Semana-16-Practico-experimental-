# Restaurante App - Semana 16

Aplicación de escritorio académica desarrollada con Python y Tkinter. Esta entrega evoluciona el proyecto de la Semana 15: conserva inicio/cierre de sesión, navegación, productos y ventas, y añade gestión administrativa de usuarios basada en eventos.

## Funcionalidades

- Inicio de sesión y navegación por Productos y Ventas.
- Gestión de productos y registro de ventas con actualización de stock.
- CRUD de usuarios (registrar, consultar al seleccionarlos, actualizar y eliminar) disponible únicamente para el rol **Administrador**.
- Roles **Administrador**, **Empleado** y **Cliente**. El administrador crea cuentas de Empleado o Cliente; no se permite eliminar la cuenta actualmente autenticada.
- `datos/usuarios.json` conserva los usuarios y sus roles. Los registros existentes sin rol se migran asignando Administrador al primer usuario y Cliente a los siguientes.
- En este modelo la identificación también funciona como nombre de usuario. La tabla muestra identificación, nombre, usuario y rol; nunca presenta la contraseña.
- `<<TreeviewSelect>>` se conecta mediante `bind()` y obtiene el identificador seleccionado para consultar el usuario a través de `RestauranteServicio`.
- `<Return>` registra desde el formulario y reutiliza `registrar_usuario`; `<Escape>` limpia los campos y cancela la selección. `<<ComboboxSelected>>` responde al rol elegido.
- Los botones Registrar, Actualizar, Eliminar y Limpiar usan `command=`. Los callbacks de interfaz coordinan los eventos y delegan las reglas y la persistencia a `RestauranteServicio`.
- Las cuentas Administrador no se pueden eliminar ni administrar como cuentas Empleado o Cliente. La cuenta administrativa autenticada tampoco puede cambiarse a otro rol. Si falla la escritura JSON, se revierte el cambio en memoria.
- `assets/` contiene y utiliza el logotipo y el icono de ventas.

## Estructura

```text
restaurante_app/
├── assets/                 # Logotipo e icono de ventas (PNG)
├── datos/                  # productos.json, usuarios.json y ventas.json
├── modelos/                # Producto, Usuario y Venta
├── servicios/              # Persistencia JSON y reglas del restaurante
├── ui/                     # LoginView y MainView
├── main.py
└── README.md
```

## Ejecución

Requiere Python 3.10 o posterior. Desde la carpeta raíz:

```bash
python main.py
```

Credenciales de ejemplo:

- Identificación `0102030405`, contraseña `admin123` (Administrador)
- Identificación `0912345678`, contraseña `maria123` (Cliente)

Las contraseñas se conservan como texto en este proyecto académico.
