import tkinter as tk
from collections.abc import Callable
from pathlib import Path
from tkinter import ttk, messagebox

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Vista principal con navegación y coordinación de las operaciones."""

    def __init__(self, parent: tk.Tk, servicio: RestauranteServicio, usuario: Usuario, al_cerrar_sesion: Callable) -> None:
        super().__init__(parent, padding=16)
        self.servicio = servicio
        self.usuario_actual = usuario
        self.al_cerrar_sesion = al_cerrar_sesion
        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.precio = tk.StringVar()
        self.stock = tk.StringVar()
        self.usuario_seleccionado = tk.StringVar()
        self.producto_seleccionado = tk.StringVar()
        self._usuarios_por_etiqueta = {}
        self._productos_por_etiqueta = {}
        self.id_usuario = tk.StringVar()
        self.nombre_usuario = tk.StringVar()
        self.clave_usuario = tk.StringVar()
        self.rol_usuario = tk.StringVar(value="Cliente")
        self._id_seleccionado = None
        self._crear_interfaz(usuario)
        self.mostrar_productos()

    def _crear_interfaz(self, usuario: Usuario) -> None:
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", pady=(0, 12))
        self._logo = None
        ruta_logo = Path(__file__).resolve().parents[1] / "assets" / "logo.png"
        try:
            self._logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(encabezado, image=self._logo).pack(side="left", padx=(0, 10))
        except tk.TclError:
            pass
        ttk.Label(encabezado, text="Restaurante App", font=("Arial", 20, "bold")).pack(side="left")
        ttk.Label(encabezado, text=f"Sesión: {usuario.nombre}").pack(side="right")

        navegacion = ttk.LabelFrame(self, text="Navegación", padding=10)
        navegacion.pack(fill="x", pady=(0, 10))
        ttk.Button(navegacion, text="Productos", command=self.mostrar_productos).pack(side="left", padx=4)
        if usuario.rol == "Administrador":
            ttk.Button(navegacion, text="Usuarios", command=self.mostrar_usuarios).pack(side="left", padx=4)
        ttk.Button(navegacion, text="Ventas", command=self.mostrar_ventas).pack(side="left", padx=4)
        ttk.Button(navegacion, text="Cerrar sesión", command=self.al_cerrar_sesion).pack(side="right", padx=4)

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True)
        formulario = ttk.LabelFrame(cuerpo, text="Gestión de productos", padding=12)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        self._crear_formulario(formulario)

        resultados = ttk.LabelFrame(cuerpo, text="Información registrada", padding=12)
        resultados.pack(side="left", fill="both", expand=True)
        self.formulario = formulario
        self.formulario_usuarios = ttk.LabelFrame(cuerpo, text="Gestión de usuarios", padding=12)
        self._crear_formulario_usuarios(self.formulario_usuarios)
        self.panel_ventas = ttk.LabelFrame(resultados, text="Registrar una venta", padding=8)
        self._crear_panel_ventas(self.panel_ventas)
        self.mensaje = ttk.Label(resultados, text="Productos cargados desde productos.json.")
        self.mensaje.pack(anchor="w", pady=(0, 8))
        self.tabla = ttk.Treeview(resultados, show="headings", height=14)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    def _crear_formulario_usuarios(self, contenedor: ttk.LabelFrame) -> None:
        campos = (("Identificación / usuario", self.id_usuario), ("Nombre", self.nombre_usuario), ("Contraseña", self.clave_usuario))
        for fila, (etiqueta, variable) in enumerate(campos):
            ttk.Label(contenedor, text=etiqueta + ":").grid(row=fila, column=0, sticky="w", pady=5)
            entrada = ttk.Entry(contenedor, textvariable=variable, width=23, show="*" if fila == 2 else "")
            entrada.grid(row=fila, column=1, pady=5)
            entrada.bind("<Return>", self._atajo_registrar_usuario)
            entrada.bind("<Escape>", self._atajo_limpiar_usuario)
        ttk.Label(contenedor, text="Rol:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_rol = ttk.Combobox(contenedor, textvariable=self.rol_usuario, values=("Empleado", "Cliente"), state="readonly", width=20)
        self.combo_rol.grid(row=3, column=1, pady=5)
        self.combo_rol.bind("<<ComboboxSelected>>", self._al_cambiar_rol)
        acciones = ttk.LabelFrame(contenedor, text="Acciones", padding=6)
        acciones.grid(row=4, column=0, columnspan=2, pady=8, sticky="ew")
        ttk.Button(acciones, text="Registrar", command=self.registrar_usuario).grid(row=0, column=0, padx=2, pady=3)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar_usuario).grid(row=0, column=1, padx=2, pady=3)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar_usuario).grid(row=1, column=0, padx=2, pady=3)
        ttk.Button(acciones, text="Limpiar", command=self.limpiar_usuario).grid(row=1, column=1, padx=2, pady=3)

    def _crear_formulario(self, contenedor: ttk.LabelFrame) -> None:
        campos = (("Código", self.codigo), ("Nombre", self.nombre), ("Precio", self.precio), ("Stock", self.stock))
        for fila, (etiqueta, variable) in enumerate(campos):
            ttk.Label(contenedor, text=f"{etiqueta}:").grid(row=fila, column=0, sticky="w", pady=5)
            ttk.Entry(contenedor, textvariable=variable, width=22).grid(row=fila, column=1, pady=5)
        acciones = ttk.LabelFrame(contenedor, text="Acciones", padding=8)
        acciones.grid(row=4, column=0, columnspan=2, pady=(12, 0), sticky="ew")
        ttk.Button(acciones, text="Registrar", command=self.registrar).grid(row=0, column=0, padx=3, pady=3)
        ttk.Button(acciones, text="Consultar", command=self.consultar).grid(row=0, column=1, padx=3, pady=3)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar).grid(row=1, column=0, padx=3, pady=3)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar).grid(row=1, column=1, padx=3, pady=3)
        ttk.Button(contenedor, text="Limpiar formulario", command=self.limpiar_formulario).grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def _preparar_tabla(self, columnas: tuple[str, ...]) -> None:
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = columnas
        for columna in columnas:
            self.tabla.heading(columna, text=columna.capitalize())
            self.tabla.column(columna, width=140, anchor="center")

    def mostrar_productos(self) -> None:
        self.formulario_usuarios.pack_forget()
        self.panel_ventas.pack_forget()
        self.formulario.pack(side="left", fill="y", padx=(0, 12))
        self._preparar_tabla(("código", "nombre", "precio", "stock"))
        for producto in self.servicio.listar_productos():
            self.tabla.insert("", "end", values=(producto.codigo, producto.nombre, f"${producto.precio:.2f}", producto.stock))
        self.mensaje.configure(text=f"Productos registrados: {self.servicio.consultar_cantidad_productos()}")

    def mostrar_usuarios(self) -> None:
        if self.usuario_actual.rol != "Administrador":
            self.mensaje.configure(text="Solo un Administrador puede gestionar usuarios.")
            return
        self.panel_ventas.pack_forget()
        self.formulario.pack_forget()
        self.formulario_usuarios.pack(side="left", fill="y", padx=(0, 12))
        self._preparar_tabla(("identificación", "nombre", "usuario", "rol"))
        for usuario in self.servicio.listar_usuarios():
            self.tabla.insert("", "end", iid=usuario.identificacion, values=(usuario.identificacion, usuario.nombre, usuario.identificacion, usuario.rol))
        self.mensaje.configure(text=f"Usuarios registrados: {self.servicio.consultar_cantidad_usuarios()}")

    def mostrar_ventas(self) -> None:
        self.formulario_usuarios.pack_forget()
        self.formulario.pack_forget()
        self.panel_ventas.pack(fill="x", pady=(0, 8), before=self.mensaje)
        self._preparar_tabla(("fecha", "usuario", "producto", "cantidad"))
        usuarios = {u.identificacion: u.nombre for u in self.servicio.listar_usuarios()}
        productos = {p.codigo: p.nombre for p in self.servicio.listar_productos()}
        for venta in self.servicio.listar_ventas():
            self.tabla.insert("", "end", values=(
                venta.fecha.replace("T", " "), usuarios.get(venta.usuario_id, venta.usuario_id),
                productos.get(venta.producto_codigo, venta.producto_codigo), venta.cantidad,
            ))
        self._actualizar_opciones_venta()
        self.mensaje.configure(text=f"Ventas registradas: {len(self.servicio.listar_ventas())}")

    def _actualizar_opciones_venta(self) -> None:
        usuarios = self.servicio.listar_usuarios()
        productos = [p for p in self.servicio.listar_productos() if p.stock > 0]
        self._usuarios_por_etiqueta = {f"{u.nombre} ({u.identificacion})": u for u in usuarios}
        self._productos_por_etiqueta = {f"{p.nombre} ({p.codigo}) · ${p.precio:.2f} · stock {p.stock}": p for p in productos}
        self.combo_usuarios["values"] = list(self._usuarios_por_etiqueta)
        self.combo_productos["values"] = list(self._productos_por_etiqueta)
        if self.usuario_seleccionado.get() not in self._usuarios_por_etiqueta:
            self.usuario_seleccionado.set("")
        if self.producto_seleccionado.get() not in self._productos_por_etiqueta:
            self.producto_seleccionado.set("")

    def _callback_registrar_venta(self) -> None:
        usuario = self._usuarios_por_etiqueta.get(self.usuario_seleccionado.get())
        producto = self._productos_por_etiqueta.get(self.producto_seleccionado.get())
        if usuario is None or producto is None:
            self.mensaje.configure(text="Seleccione un usuario y un producto disponible.")
            return
        try:
            venta = self.servicio.registrar_venta(usuario.identificacion, producto.codigo)
            self.mostrar_ventas()
            self.mensaje.configure(text=f"Venta registrada correctamente para {usuario.nombre}: {producto.nombre}.")
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def _crear_panel_ventas(self, contenedor: ttk.LabelFrame) -> None:
        ruta_icono = Path(__file__).resolve().parents[1] / "assets" / "icono_ventas.png"
        try:
            self._icono_ventas = tk.PhotoImage(file=str(ruta_icono))
            ttk.Label(contenedor, image=self._icono_ventas).grid(row=0, column=2, rowspan=3, padx=12)
        except tk.TclError:
            self._icono_ventas = None
        self.combo_usuarios = ttk.Combobox(contenedor, textvariable=self.usuario_seleccionado, state="readonly", width=35)
        self.combo_productos = ttk.Combobox(contenedor, textvariable=self.producto_seleccionado, state="readonly", width=42)
        ttk.Label(contenedor, text="Usuario:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.combo_usuarios.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(contenedor, text="Producto disponible:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.combo_productos.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        contenedor.columnconfigure(1, weight=1)
        ttk.Button(contenedor, text="Registrar venta", command=self._callback_registrar_venta).grid(row=2, column=1, sticky="e", padx=4, pady=8)

    def registrar(self) -> None:
        self._ejecutar_operacion(self.servicio.registrar_producto, "Producto registrado correctamente.")

    def actualizar(self) -> None:
        self._ejecutar_operacion(self.servicio.actualizar_producto, "Producto actualizado correctamente.")

    def eliminar(self) -> None:
        try:
            self.servicio.eliminar_producto(self.codigo.get())
            self.limpiar_formulario()
            self.mostrar_productos()
            self.mensaje.configure(text="Producto eliminado correctamente.")
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def consultar(self) -> None:
        producto = self.servicio.consultar_producto(self.codigo.get())
        if producto is None:
            self.mensaje.configure(text="No se encontró un producto con ese código.")
            return
        self.nombre.set(producto.nombre)
        self.precio.set(str(producto.precio))
        self.stock.set(str(producto.stock))
        self.mensaje.configure(text="Producto cargado en el formulario.")

    def _ejecutar_operacion(self, operacion: Callable, exito: str) -> None:
        try:
            operacion(self.codigo.get(), self.nombre.get(), self.precio.get(), self.stock.get())
            self.mostrar_productos()
            self.mensaje.configure(text=exito)
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def limpiar_formulario(self) -> None:
        self.codigo.set("")
        self.nombre.set("")
        self.precio.set("")
        self.stock.set("")

    def _al_seleccionar_fila(self, event=None) -> None:
        if self.tabla["columns"] != ("identificación", "nombre", "usuario", "rol"):
            return
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        usuario = self.servicio.consultar_usuario(seleccion[0])
        if usuario is None:
            return
        self._id_seleccionado = usuario.identificacion
        self.id_usuario.set(usuario.identificacion)
        self.nombre_usuario.set(usuario.nombre)
        self.clave_usuario.set(usuario.contrasena)
        self.rol_usuario.set(usuario.rol)
        self.mensaje.configure(text="Usuario cargado en el formulario.")

    def _atajo_registrar_usuario(self, event=None):
        self.registrar_usuario()
        return "break"

    def _atajo_limpiar_usuario(self, event=None):
        self.limpiar_usuario()
        return "break"

    def _al_cambiar_rol(self, event=None) -> None:
        self.mensaje.configure(text=f"Rol seleccionado: {self.rol_usuario.get()}.")

    def registrar_usuario(self) -> None:
        try:
            self.servicio.registrar_usuario(self.id_usuario.get(), self.nombre_usuario.get(), self.clave_usuario.get(), self.rol_usuario.get())
            self.mostrar_usuarios()
            self.limpiar_usuario()
            self.mensaje.configure(text="Usuario registrado correctamente.")
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def actualizar_usuario(self) -> None:
        if not self._id_seleccionado:
            self.mensaje.configure(text="Seleccione un usuario para actualizar.")
            return
        try:
            self.servicio.actualizar_usuario(
                self._id_seleccionado,
                self.nombre_usuario.get(),
                self.clave_usuario.get(),
                self.rol_usuario.get(),
                administrador_actual=self.usuario_actual.identificacion,
            )
            self.mostrar_usuarios()
            self.limpiar_usuario()
            self.mensaje.configure(text="Usuario actualizado correctamente.")
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def eliminar_usuario(self) -> None:
        if not self._id_seleccionado:
            self.mensaje.configure(text="Seleccione un usuario para eliminar.")
            return
        if not messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el usuario seleccionado?", parent=self):
            return
        try:
            self.servicio.eliminar_usuario(self._id_seleccionado, self.usuario_actual.identificacion)
            self.mostrar_usuarios()
            self.limpiar_usuario()
            self.mensaje.configure(text="Usuario eliminado correctamente.")
        except ValueError as error:
            self.mensaje.configure(text=f"Error: {error}")

    def limpiar_usuario(self) -> None:
        self._id_seleccionado = None
        self.id_usuario.set("")
        self.nombre_usuario.set("")
        self.clave_usuario.set("")
        self.rol_usuario.set("Cliente")
        if hasattr(self, "tabla") and self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())
