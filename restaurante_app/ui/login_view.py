import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    def __init__(self, parent: tk.Tk, servicio: RestauranteServicio, al_ingresar: Callable) -> None:
        super().__init__(parent, padding=30)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text="Restaurante App", font=("Arial", 18, "bold")).grid(row=0, column=0, pady=(0, 8))
        ttk.Label(self, text="Ingrese sus credenciales para continuar").grid(row=1, column=0, pady=(0, 20))
        formulario = ttk.Frame(self)
        formulario.grid(row=2, column=0)
        ttk.Label(formulario, text="Identificación:").grid(row=0, column=0, sticky="w", pady=5)
        self.identificacion_entry = ttk.Entry(formulario, width=28)
        self.identificacion_entry.grid(row=0, column=1, pady=5)
        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
        self.contrasena_entry = ttk.Entry(formulario, width=28, show="*")
        self.contrasena_entry.grid(row=1, column=1, pady=5)
        self.contrasena_entry.bind("<Return>", lambda evento: self.ingresar())
        self.mensaje = ttk.Label(self, foreground="firebrick")
        self.mensaje.grid(row=3, column=0, pady=(10, 5))
        ttk.Button(self, text="Ingresar", command=self.ingresar).grid(row=4, column=0, pady=8)
        self.identificacion_entry.focus()

    def ingresar(self) -> None:
        identificacion = self.identificacion_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        if not identificacion or not contrasena:
            self.mensaje.configure(text="Ingrese identificación y contraseña.")
            return
        usuario = self.servicio.validar_acceso(identificacion, contrasena)
        if usuario is None:
            self.mensaje.configure(text="Credenciales incorrectas.")
            return
        self.al_ingresar(usuario)
