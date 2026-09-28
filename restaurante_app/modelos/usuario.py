class Usuario:
    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion: str, nombre: str, contrasena: str, rol: str = "Cliente") -> None:
        if not identificacion.strip():
            raise ValueError("La identificación no puede estar vacía.")

        if not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")

        if not contrasena.strip():
            raise ValueError("La contraseña no puede estar vacía.")
        if rol not in self.ROLES:
            raise ValueError("Seleccione un rol válido.")

        self.identificacion = identificacion
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Usuario":
        try:
            identificacion = datos["identificacion"]
            nombre = datos["nombre"]
            contrasena = datos["contrasena"]
        except KeyError as error:
            raise KeyError(f"Falta la clave: {error.args[0]}")

        return cls(identificacion, nombre, contrasena, datos.get("rol", "Cliente"))

    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre}"
