from __future__ import annotations

import json

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, ruta: str) -> None:
        self.ruta = ruta

    def guardar_productos(self, productos: list[Producto]) -> None:
        datos = [producto.to_dict() for producto in productos]

        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)

        except PermissionError:
            print("Error: no existen permisos para escribir el archivo.")

    def cargar_productos(self) -> list[Producto]:
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            productos = []

            for registro in datos:
                try:
                    producto = Producto.from_dict(registro)
                    productos.append(producto)
                except (KeyError, ValueError) as error:
                    print(f"Registro inválido: {error}")

            return productos

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Error: el archivo JSON no tiene un formato válido.")
            return []

        except PermissionError:
            print("Error: no existen permisos para leer el archivo.")
            return []

    def guardar_usuarios(
        self,
        usuarios: list[Usuario],
        ruta: str | None = None
    ) -> None:
        datos = [usuario.to_dict() for usuario in usuarios]
        destino = ruta or self.ruta
        with open(destino, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar_usuarios(
        self,
        ruta: str | None = None
    ) -> list[Usuario]:
        destino = ruta or self.ruta
        try:
            with open(destino, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            usuarios = []

            for indice, registro in enumerate(datos):
                try:
                    registro.setdefault("rol", "Administrador" if indice == 0 else "Cliente")
                    usuario = Usuario.from_dict(registro)
                    usuarios.append(usuario)
                except (KeyError, ValueError) as error:
                    print(f"Registro de usuario inválido: {error}")

            return usuarios

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Error: el archivo JSON de usuarios no es válido.")
            return []

        except PermissionError:
            print("Error: no existen permisos para leer usuarios.")

    def guardar_ventas(
        self,
        ventas: list[Venta],
        ruta: str | None = None
    ) -> None:
        datos = [venta.to_dict() for venta in ventas]
        destino = ruta or self.ruta
        with open(destino, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar_ventas(
        self,
        ruta: str | None = None
    ) -> list[Venta]:
        destino = ruta or self.ruta
        try:
            with open(destino, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            ventas = []

            for registro in datos:
                try:
                    venta = Venta.from_dict(registro)
                    ventas.append(venta)
                except (KeyError, ValueError) as error:
                    print(f"Registro de venta inválido: {error}")

            return ventas

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Error: el archivo JSON de ventas no es válido.")
            return []

        except PermissionError:
            print("Error: no existen permisos para leer ventas.")
            return []
