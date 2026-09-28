from pathlib import Path
import tkinter as tk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    """Configura los servicios y coordina las vistas de la aplicación."""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent
        ruta_datos = base_dir / "datos"
        archivo_productos = ArchivoServicio(ruta_datos / "productos.json")
        archivo_usuarios = ArchivoServicio(ruta_datos / "usuarios.json")
        archivo_ventas = ArchivoServicio(ruta_datos / "ventas.json")

        productos = archivo_productos.cargar_productos()
        usuarios = archivo_usuarios.cargar_usuarios()
        ventas = archivo_ventas.cargar_ventas()
        self.servicio = RestauranteServicio(
            productos, usuarios, archivo_productos, ventas, archivo_ventas,
            archivo_usuarios=archivo_usuarios,
        )

        self.root = tk.Tk()
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("900x620")
        self.root.minsize(820, 560)
        self.vista_actual = None
        self.mostrar_login()

    def cambiar_vista(self, vista: tk.Widget) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self.cambiar_vista(
            LoginView(self.root, self.servicio, self.mostrar_principal)
        )

    def mostrar_principal(self, usuario: Usuario) -> None:
        self.cambiar_vista(
            MainView(self.root, self.servicio, usuario, self.mostrar_login)
        )

    def ejecutar(self) -> None:
        self.root.mainloop()


def main() -> None:
    AplicacionRestaurante().ejecutar()


if __name__ == "__main__":
    main()
