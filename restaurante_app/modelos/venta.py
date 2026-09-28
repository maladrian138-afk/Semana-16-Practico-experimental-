from datetime import datetime


class Venta:
    """Registro de una compra realizada por un usuario."""

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int = 1,
        fecha: str | None = None,
    ) -> None:
        if not usuario_id.strip():
            raise ValueError("Seleccione un usuario.")
        if not producto_codigo.strip():
            raise ValueError("Seleccione un producto.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.fecha = fecha or datetime.now().astimezone().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Venta":
        return cls(
            datos["usuario_id"],
            datos["producto_codigo"],
            int(datos.get("cantidad", 1)),
            datos.get("fecha"),
        )
