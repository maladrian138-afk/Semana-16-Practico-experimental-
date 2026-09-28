from servicios.archivo_servicio import ArchivoServicio
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Coordina los datos del restaurante sin depender de la interfaz."""

    def __init__(
        self,
        productos: list[Producto],
        usuarios: list[Usuario],
        archivo_productos: ArchivoServicio,
        ventas: list[Venta] | None = None,
        archivo_ventas: ArchivoServicio | None = None,
        archivo_usuarios: ArchivoServicio | None = None,
    ) -> None:
        self._productos = productos
        self._usuarios = usuarios
        self._archivo_productos = archivo_productos
        self._ventas = ventas or []
        self._archivo_ventas = archivo_ventas
        self._archivo_usuarios = archivo_usuarios

    def validar_acceso(self, identificacion: str, contrasena: str) -> Usuario | None:
        identificacion = identificacion.strip()
        contrasena = contrasena.strip()
        if not identificacion or not contrasena:
            return None
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion and usuario.contrasena == contrasena:
                return usuario
        return None

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def consultar_usuario(self, identificacion: str) -> Usuario | None:
        return next((u for u in self._usuarios if u.identificacion == identificacion), None)

    def registrar_usuario(self, identificacion: str, nombre: str, contrasena: str, rol: str) -> Usuario:
        if self.consultar_usuario(identificacion.strip()) is not None:
            raise ValueError("Ya existe un usuario con esa identificación.")
        usuario = Usuario(identificacion.strip(), nombre.strip(), contrasena, rol)
        self._usuarios.append(usuario)
        try:
            self._guardar_usuarios()
        except ValueError:
            self._usuarios.remove(usuario)
            raise
        return usuario

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        contrasena: str,
        rol: str,
        administrador_actual: str | None = None,
    ) -> Usuario:
        usuario = self.consultar_usuario(identificacion.strip())
        if usuario is None:
            raise ValueError("No existe un usuario con esa identificación.")
        if usuario.rol == "Administrador" and usuario.identificacion != administrador_actual:
            raise ValueError("La gestión está habilitada para usuarios Empleado y Cliente.")
        if usuario.identificacion == administrador_actual and rol != "Administrador":
            raise ValueError("No puede cambiar el rol de la cuenta administrativa con sesión activa.")
        actualizado = Usuario(identificacion.strip(), nombre.strip(), contrasena, rol)
        anterior = (usuario.nombre, usuario.contrasena, usuario.rol)
        usuario.nombre, usuario.contrasena, usuario.rol = actualizado.nombre, actualizado.contrasena, actualizado.rol
        try:
            self._guardar_usuarios()
        except ValueError:
            usuario.nombre, usuario.contrasena, usuario.rol = anterior
            raise
        return usuario

    def eliminar_usuario(self, identificacion: str, administrador_actual: str) -> None:
        usuario = self.consultar_usuario(identificacion.strip())
        if usuario is None:
            raise ValueError("No existe el usuario seleccionado.")
        if usuario.rol == "Administrador":
            if usuario.identificacion == administrador_actual:
                raise ValueError("No puede eliminar la cuenta administrativa con sesión activa.")
            raise ValueError("La gestión está habilitada para usuarios Empleado y Cliente.")
        self._usuarios.remove(usuario)
        try:
            self._guardar_usuarios()
        except ValueError:
            self._usuarios.append(usuario)
            raise

    def _guardar_usuarios(self) -> None:
        if self._archivo_usuarios is None:
            raise ValueError("No está configurado el archivo de usuarios.")
        try:
            self._archivo_usuarios.guardar_usuarios(self._usuarios, self._archivo_usuarios.ruta)
        except OSError as error:
            raise ValueError(f"No se pudieron guardar los usuarios: {error}") from error

    def consultar_cantidad_productos(self) -> int:
        return len(self._productos)

    def consultar_cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    def listar_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def registrar_venta(self, usuario_id: str, producto_codigo: str) -> Venta:
        usuario = next((u for u in self._usuarios if u.identificacion == usuario_id), None)
        if usuario is None:
            raise ValueError("El usuario seleccionado ya no está disponible.")
        producto = self._buscar_producto(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado ya no está disponible.")
        producto.vender(1)
        venta = Venta(usuario.identificacion, producto.codigo)
        self._ventas.append(venta)
        try:
            self._guardar_productos()
            if self._archivo_ventas is None:
                raise ValueError("No está configurado el archivo de ventas.")
            self._archivo_ventas.guardar_ventas(self._ventas)
        except OSError as error:
            self._ventas.remove(venta)
            producto.stock += 1
            raise ValueError(f"No se pudo guardar la venta: {error}") from error
        return venta

    def _buscar_producto(self, codigo: str) -> Producto | None:
        codigo_normalizado = codigo.strip().lower()
        for producto in self._productos:
            if producto.codigo.strip().lower() == codigo_normalizado:
                return producto
        return None

    def consultar_producto(self, codigo: str) -> Producto | None:
        return self._buscar_producto(codigo)

    def registrar_producto(self, codigo: str, nombre: str, precio: str, stock: str) -> Producto:
        if self._buscar_producto(codigo) is not None:
            raise ValueError("Ya existe un producto con ese código.")
        producto = Producto(codigo.strip(), nombre.strip(), float(precio), int(stock))
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, codigo: str, nombre: str, precio: str, stock: str) -> Producto:
        producto = self._buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        producto_actualizado = Producto(codigo.strip(), nombre.strip(), float(precio), int(stock))
        producto.nombre = producto_actualizado.nombre
        producto.precio = producto_actualizado.precio
        producto.stock = producto_actualizado.stock
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> None:
        producto = self._buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        self._productos.remove(producto)
        self._guardar_productos()

    def _guardar_productos(self) -> None:
        self._archivo_productos.guardar_productos(self._productos)
