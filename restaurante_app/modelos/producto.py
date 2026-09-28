class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int) -> None:
        if not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")

        if not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")

        self.stock -= cantidad

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        try:
            codigo = datos["codigo"]
            nombre = datos["nombre"]
            precio = float(datos["precio"])
            stock = int(datos["stock"])
        except KeyError as error:
            raise KeyError(f"Falta la clave: {error.args[0]}")

        return cls(codigo, nombre, precio, stock)

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} - ${self.precio:.2f} - Stock: {self.stock}"