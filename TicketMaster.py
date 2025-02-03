import tkinter as tk
from tkinter import messagebox, simpledialog
import re
from datetime import datetime

# Clase para representar un usuario
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Lista para almacenar usuarios (en memoria)
usuarios = []

# Función para validar el formato del usuario y contraseña
def validar_formato(texto):
    if not texto.islower():
        return False, "Solo se permiten minúsculas."
    if any(caracter.isdigit() for caracter in texto):
        return False, "No se permiten números."
    
    caracteres_especiales = re.findall(r'[^\w\s]', texto)
    if caracteres_especiales:
        for caracter in caracteres_especiales:
            if not (texto.startswith(caracter) or texto.endswith(caracter)):
                return False, "Los caracteres especiales solo pueden estar al inicio o al final."
    return True, ""

# Función para verificar si un año es bisiesto
def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

# Función para verificar si una fecha es festiva
def es_dia_festivo(dia, mes, anio):
    dias_festivos = [
        (1, 1), (3, 2), (17, 3), (17, 4),
        (18, 4), (1, 5), (16, 9), (17, 11), (25, 12)
    ]
    return (dia, mes) in dias_festivos



# Pantalla de inicio de sesión
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Iniciar Sesión")
        self.root.geometry("400x300")

        self.label_username = tk.Label(root, text="Usuario:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(root, text="Contraseña:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=10)

        self.button_login = tk.Button(root, text="Iniciar Sesión", command=self.login)
        self.button_login.pack(pady=20)
        self.button_register = tk.Button(root, text="Registrarse", command=self.open_register)
        self.button_register.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        for usuario in usuarios:
            if usuario.username == username and usuario.password == password:
                self.root.destroy()
                open_main_menu()
                return
        messagebox.showerror("Error", "Credenciales incorrectas.")

    def open_register(self):
        self.root.destroy()
        open_register_screen()

# Pantalla de registro
class RegisterScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Registro")
        self.root.geometry("400x300")

        self.label_new_username = tk.Label(root, text="Nuevo Usuario:")
        self.label_new_username.pack(pady=10)
        self.entry_new_username = tk.Entry(root)
        self.entry_new_username.pack(pady=10)

        self.label_new_password = tk.Label(root, text="Nueva Contraseña:")
        self.label_new_password.pack(pady=10)
        self.entry_new_password = tk.Entry(root, show="*")
        self.entry_new_password.pack(pady=10)

        self.button_register = tk.Button(root, text="Registrar", command=self.register)
        self.button_register.pack(pady=20)
        self.button_back = tk.Button(root, text="Volver", command=self.back_to_login)
        self.button_back.pack(pady=10)

    def register(self):
        username = self.entry_new_username.get()
        password = self.entry_new_password.get()

        valido, mensaje = validar_formato(username)
        if not valido:
            messagebox.showerror("Error", f"Usuario inválido: {mensaje}")
            return

        valido, mensaje = validar_formato(password)
        if not valido:
            messagebox.showerror("Error", f"Contraseña inválida: {mensaje}")
            return

        for usuario in usuarios:
            if usuario.username == username:
                messagebox.showerror("Error", "El usuario ya existe.")
                return

        usuarios.append(Usuario(username, password))
        messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
        self.back_to_login()

    def back_to_login(self):
        self.root.destroy()
        open_login_screen()

# Menú principal
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Menú Principal")
        self.root.geometry("400x300")

        self.label_welcome = tk.Label(root, text="¡Bienvenido!")
        self.label_welcome.pack(pady=20)

        self.button_teatro = tk.Button(root, text="Teatro", command=self.open_teatro)
        self.button_teatro.pack(pady=10)
        self.button_cine = tk.Button(root, text="Cine", command=self.open_cine)
        self.button_cine.pack(pady=10)
        self.button_museo = tk.Button(root, text="Museo", command=self.open_museo)
        self.button_museo.pack(pady=10)
        self.button_salir = tk.Button(root, text="Salir", command=self.salir)
        self.button_salir.pack(pady=10)

    def open_teatro(self):
        self.root.destroy()
        open_teatro_screen()

    def open_cine(self):
        self.root.destroy()
        open_cine_screen()

    def open_museo(self):
        self.root.destroy()
        open_museo_screen()

    def salir(self):
        self.root.destroy()

# Pantalla de Teatro
class TeatroScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Teatro")
        self.root.geometry("500x400")

        self.label_teatro = tk.Label(root, text="Seleccione un teatro:")
        self.label_teatro.pack(pady=10)

        self.teatros = ["Elija una opción", "Teatro Colón (Buenos Aires)", 
                       "Teatro de la Scala (Milán)", "Teatro Metropólitan (Ciudad de México)"]
        self.combo_teatro = tk.StringVar(root)
        self.combo_teatro.set(self.teatros[0])
        self.dropdown_teatro = tk.OptionMenu(root, self.combo_teatro, *self.teatros)
        self.dropdown_teatro.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def continuar(self):
        teatro_seleccionado = self.combo_teatro.get()
        if teatro_seleccionado == "Elija una opción":
            messagebox.showerror("Error", "Debes seleccionar un teatro.")
            return

        self.root.destroy()
        open_teatro_detalle(teatro_seleccionado)

    def volver(self):
        self.root.destroy()
        open_main_menu()

class TeatroDetalleScreen:
    def __init__(self, root, teatro):
        self.root = root
        self.root.title("TicketMaster - Detalles del Teatro")
        self.root.geometry("600x500")

        self.teatro = teatro
        self.capacidad = self.obtener_capacidad(teatro)

        self.label_teatro = tk.Label(root, text=f"Teatro: {teatro}")
        self.label_teatro.pack(pady=10)
        self.label_capacidad = tk.Label(root, text=f"Capacidad: {self.capacidad} personas")
        self.label_capacidad.pack(pady=10)

        # Campos de entrada
        self.label_fecha = tk.Label(root, text="Fecha (dd/mm/aaaa):")
        self.label_fecha.pack(pady=10)
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.pack(pady=10)

        self.label_obra = tk.Label(root, text="Obra:")
        self.label_obra.pack(pady=10)
        self.obras = ["Elija una opción", "El rey León", "Frankenstein", "Romeo y Julieta"]
        self.combo_obra = tk.StringVar(root)
        self.combo_obra.set(self.obras[0])
        self.dropdown_obra = tk.OptionMenu(root, self.combo_obra, *self.obras)
        self.dropdown_obra.pack(pady=10)

        self.label_horario = tk.Label(root, text="Horario:")
        self.label_horario.pack(pady=10)
        self.horarios = ["Elija una opción", "3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM", "5:00 PM - 6:00 PM"]
        self.combo_horario = tk.StringVar(root)
        self.combo_horario.set(self.horarios[0])
        self.dropdown_horario = tk.OptionMenu(root, self.combo_horario, *self.horarios)
        self.dropdown_horario.pack(pady=10)

        self.label_seccion = tk.Label(root, text="Sección:")
        self.label_seccion.pack(pady=10)
        self.secciones = ["Elija una opción", "Luneta ($500)", "Palco ($800)", "Galería ($300)"]
        self.combo_seccion = tk.StringVar(root)
        self.combo_seccion.set(self.secciones[0])
        self.dropdown_seccion = tk.OptionMenu(root, self.combo_seccion, *self.secciones)
        self.dropdown_seccion.pack(pady=10)

        self.label_boletos = tk.Label(root, text="Cantidad de boletos (1-10):")
        self.label_boletos.pack(pady=10)
        self.entry_boletos = tk.Entry(root)
        self.entry_boletos.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def obtener_capacidad(self, teatro):
        capacidades = {
            "Teatro Colón (Buenos Aires)": 2500,
            "Teatro de la Scala (Milán)": 2800,
            "Teatro Metropólitan (Ciudad de México)": 8000
        }
        return capacidades.get(teatro, 0)

    def continuar(self):
        # Validaciones
        try:
            fecha = self.entry_fecha.get()
            dia, mes, anio = map(int, fecha.split('/'))
            
            if not (1 <= mes <= 12):
                raise ValueError("Mes inválido")
            
            dias_mes = [31,29 if es_bisiesto(anio) else 28,31,30,31,30,31,31,30,31,30,31]
            if not (1 <= dia <= dias_mes[mes-1]):
                raise ValueError("Día inválido")
            
            if es_dia_festivo(dia, mes, anio):
                raise ValueError("Día festivo no permitido")

        except Exception as e:
            messagebox.showerror("Error", f"Fecha inválida: {str(e)}")
            return

        # Validar selecciones
        if (self.combo_obra.get() == "Elija una opción" or 
            self.combo_horario.get() == "Elija una opción" or 
            self.combo_seccion.get() == "Elija una opción"):
            messagebox.showerror("Error", "Seleccione todas las opciones")
            return

        # Validar boletos
        try:
            boletos = int(self.entry_boletos.get())
            if not (1 <= boletos <= 10):
                raise ValueError("Cantidad inválida")
        except:
            messagebox.showerror("Error", "Cantidad de boletos inválida")
            return

        # Calcular total
        precios = {"Luneta":500, "Palco":800, "Galería":300}
        seccion = self.combo_seccion.get().split()[0]
        total = precios[seccion] * boletos

        # Construir resumen
        resumen = f"""--- Resumen de la Compra ---
Teatro: {self.teatro}
Obra: {self.combo_obra.get()}
Fecha: {fecha}
Horario: {self.combo_horario.get()}
Sección: {self.combo_seccion.get()}
Cantidad de boletos: {boletos}
Total a pagar: ${total}
Tipo de vestimenta: Formal (Traje o vestido elegante)"""

        # Método de pago
        metodo_pago = self.solicitar_metodo_pago()
        if not metodo_pago:
            return

        # Datos de pago
        datos_pago = self.solicitar_datos_pago(metodo_pago)
        if not datos_pago:
            return

        resumen += f"\nMétodo de pago: {metodo_pago}"
        resumen += f"\nDatos de pago: {datos_pago}"

        # Mostrar resumen
        self.root.destroy()
        root = tk.Tk()
        ResumenScreen(root, resumen)
        # root.mainloop()

    def solicitar_metodo_pago(self):
        ventana = tk.Toplevel()
        ventana.title("Método de Pago")
        metodo = tk.StringVar(value="tarjeta de crédito")
        
        tk.Label(ventana, text="Seleccione método de pago:").pack(pady=10)
        opciones = [
            ("Tarjeta de Crédito", "tarjeta de crédito"),
            ("Tarjeta de Débito", "tarjeta de débito"),
            ("PayPal", "paypal")
        ]
        
        for texto, valor in opciones:
            tk.Radiobutton(ventana, text=texto, variable=metodo, value=valor).pack()
        
        confirmado = [False]
        def confirmar():
            confirmado[0] = True
            ventana.destroy()
        
        tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        ventana.wait_window()
        
        return metodo.get() if confirmado[0] else None

    def solicitar_datos_pago(self, metodo):
        ventana = tk.Toplevel(self.root)
        ventana.title("Datos de Pago")
        ventana.geometry("300x150")
    
        # Variables para almacenar los datos
        nombre = tk.StringVar()
        detalle = tk.StringVar()
        resultado = None
    
        # Configurar la ventana
        tk.Label(ventana, text="Nombre del titular:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(ventana, textvariable=nombre)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    
        etiqueta = "Correo de PayPal:" if metodo == "paypal" else "Número de tarjeta:"
        tk.Label(ventana, text=etiqueta).grid(row=1, column=0, padx=10, pady=5)
        entry_detalle = tk.Entry(ventana, textvariable=detalle)
        entry_detalle.grid(row=1, column=1, padx=10, pady=5)
    
        def confirmar():
            nonlocal resultado
            if nombre.get().strip() and detalle.get().strip():
                if metodo == "paypal":
                    resultado = f"Nombre: {nombre.get().strip()}, Correo: {detalle.get().strip()}"
                else:
                    resultado = f"Nombre: {nombre.get().strip()}, Tarjeta: {detalle.get().strip()}"
                
                # Mostrar un mensaje si el dato es incorrecto
                if metodo == "paypal" and "@" not in detalle.get().strip():
                    messagebox.showerror("Error", "El correo de PayPal es incorrecto. Por favor, corríjalo.")
                elif metodo != "paypal" and len(detalle.get().strip()) < 13:
                    messagebox.showerror("Error", "El número de tarjeta es incorrecto. Debe tener al menos 13 caracteres.")
                else:
                    ventana.destroy()  # Si todo es correcto, cerramos la ventana
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios. Por favor, complete los datos.")

        btn_confirmar = tk.Button(ventana, text="Confirmar", command=confirmar)
        btn_confirmar.grid(row=2, columnspan=2, pady=10)
    
        # Hacer la ventana modal y esperar
        ventana.grab_set()
        ventana.wait_window()
    
        return resultado

    def volver(self):
        self.root.destroy()
        open_teatro_screen()

class CineScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Cine")
        self.root.geometry("500x400")

        self.label_cine = tk.Label(root, text="Seleccione un cine:")
        self.label_cine.pack(pady=10)

        # Actualización de las opciones de cine
        self.cines = ["Elija una opción", "Cinemark", "Cinópolis", "Cinemex", "AMC"]
        self.combo_cine = tk.StringVar(root)
        self.combo_cine.set(self.cines[0])
        self.dropdown_cine = tk.OptionMenu(root, self.combo_cine, *self.cines)
        self.dropdown_cine.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def continuar(self):
        cine_seleccionado = self.combo_cine.get()
        if cine_seleccionado == "Elija una opción":
            messagebox.showerror("Error", "Debes seleccionar un cine.")
            return

        self.root.destroy()
        open_cine_detalle(cine_seleccionado)

    def volver(self):
        self.root.destroy()
        open_main_menu()

class CineDetalleScreen:
    def __init__(self, root, cine):
        self.root = root
        self.root.title("TicketMaster - Detalles del Cine")
        self.root.geometry("600x500")

        self.cine = cine
        self.capacidad = self.obtener_capacidad(cine)

        self.label_cine = tk.Label(root, text=f"Cine: {cine}")
        self.label_cine.pack(pady=10)
        self.label_capacidad = tk.Label(root, text=f"Capacidad: {self.capacidad} personas")
        self.label_capacidad.pack(pady=10)

        # Campos de entrada
        self.label_fecha = tk.Label(root, text="Fecha (dd/mm/aaaa):")
        self.label_fecha.pack(pady=10)
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.pack(pady=10)

        self.label_pelicula = tk.Label(root, text="Película:")
        self.label_pelicula.pack(pady=10)
        self.peliculas = ["Elija una opción", "Avatar 2", "Spider-Man: No Way Home", "Jurassic World"]
        self.combo_pelicula = tk.StringVar(root)
        self.combo_pelicula.set(self.peliculas[0])
        self.dropdown_pelicula = tk.OptionMenu(root, self.combo_pelicula, *self.peliculas)
        self.dropdown_pelicula.pack(pady=10)

        self.label_horario = tk.Label(root, text="Horario:")
        self.label_horario.pack(pady=10)
        self.horarios = ["Elija una opción", "1:00 PM - 3:00 PM", "3:30 PM - 5:30 PM", "6:00 PM - 8:00 PM"]
        self.combo_horario = tk.StringVar(root)
        self.combo_horario.set(self.horarios[0])
        self.dropdown_horario = tk.OptionMenu(root, self.combo_horario, *self.horarios)
        self.dropdown_horario.pack(pady=10)

        self.label_seccion = tk.Label(root, text="Sección:")
        self.label_seccion.pack(pady=10)
        self.secciones = ["Elija una opción", "Tradicional ($100.00)", "PLUUS ($120.00)", "VIP ($150.00)",
                          "Macro XE ($140.00)", "Cinópolis Junior ($110.00)", "4DX ($200.00)", "IMAX ($180.00)", 
                          "VR ($160.00)", "Screen X ($170.00)"]
        self.combo_seccion = tk.StringVar(root)
        self.combo_seccion.set(self.secciones[0])
        self.dropdown_seccion = tk.OptionMenu(root, self.combo_seccion, *self.secciones)
        self.dropdown_seccion.pack(pady=10)

        self.label_boletos = tk.Label(root, text="Cantidad de boletos (1-10):")
        self.label_boletos.pack(pady=10)
        self.entry_boletos = tk.Entry(root)
        self.entry_boletos.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def obtener_capacidad(self, cine):
        capacidades = {
            "Cinemark": 700,
            "Cinópolis": 800,
            "Cinemex": 600,
            "AMC": 900
        }
        return capacidades.get(cine, 0)


    def continuar(self):
        # Validaciones similares al proceso del teatro
        try:
            fecha = self.entry_fecha.get()
            dia, mes, anio = map(int, fecha.split('/'))
            
            if not (1 <= mes <= 12):
                raise ValueError("Mes inválido")
            
            dias_mes = [31,29 if es_bisiesto(anio) else 28,31,30,31,30,31,31,30,31,30,31]
            if not (1 <= dia <= dias_mes[mes-1]):
                raise ValueError("Día inválido")
            
            if es_dia_festivo(dia, mes, anio):
                raise ValueError("Día festivo no permitido")

        except Exception as e:
            messagebox.showerror("Error", f"Fecha inválida: {str(e)}")
            return

        # Validar selecciones
        if (self.combo_pelicula.get() == "Elija una opción" or 
            self.combo_horario.get() == "Elija una opción" or 
            self.combo_seccion.get() == "Elija una opción"):
            messagebox.showerror("Error", "Seleccione todas las opciones")
            return

        # Validar boletos
        try:
            boletos = int(self.entry_boletos.get())
            if not (1 <= boletos <= 10):
                raise ValueError("Cantidad inválida")
        except:
            messagebox.showerror("Error", "Cantidad de boletos inválida")
            return

        # Calcular total
        precios = {"Tradicional":100, "PLUUS":120, "VIP":150, "Macro XE":140, 
                   "Cinópolis Junior":110, "4DX":200, "IMAX":180, "VR":160, "Screen X":170}
        seccion = self.combo_seccion.get().split()[0]
        total = precios[seccion] * boletos

        # Construir resumen
        resumen = f"""--- Resumen de la Compra ---\n
Cine: {self.cine}
Película: {self.combo_pelicula.get()}
Fecha: {fecha}
Horario: {self.combo_horario.get()}
Sección: {self.combo_seccion.get()}
Cantidad de boletos: {boletos}
Total a pagar: ${total}
Tipo de vestimenta: Casual (ropa cómoda)"""

        # Método de pago
        metodo_pago = self.solicitar_metodo_pago()
        if not metodo_pago:
            return

        # Datos de pago
        datos_pago = self.solicitar_datos_pago(metodo_pago)
        if not datos_pago:
            return

        resumen += f"\nMétodo de pago: {metodo_pago}"
        resumen += f"\nDatos de pago: {datos_pago}"

        # Mostrar resumen
        self.root.destroy()
        root = tk.Tk()
        ResumenScreen(root, resumen)

    def solicitar_metodo_pago(self):
        ventana = tk.Toplevel()
        ventana.title("Método de Pago")
        metodo = tk.StringVar(value="tarjeta de crédito")
        
        tk.Label(ventana, text="Seleccione método de pago:").pack(pady=10)
        opciones = [
            ("Tarjeta de Crédito", "tarjeta de crédito"),
            ("Tarjeta de Débito", "tarjeta de débito"),
            ("PayPal", "paypal")
        ]
        
        for texto, valor in opciones:
            tk.Radiobutton(ventana, text=texto, variable=metodo, value=valor).pack()
        
        confirmado = [False]
        def confirmar():
            confirmado[0] = True
            ventana.destroy()
        
        tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        ventana.wait_window()
        
        return metodo.get() if confirmado[0] else None

    def solicitar_datos_pago(self, metodo):
        ventana = tk.Toplevel(self.root)
        ventana.title("Datos de Pago")
        ventana.geometry("300x150")
    
        # Variables para almacenar los datos
        nombre = tk.StringVar()
        detalle = tk.StringVar()
        resultado = None
    
        # Configurar la ventana
        tk.Label(ventana, text="Nombre del titular:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(ventana, textvariable=nombre)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    
        etiqueta = "Correo de PayPal:" if metodo == "paypal" else "Número de tarjeta:"
        tk.Label(ventana, text=etiqueta).grid(row=1, column=0, padx=10, pady=5)
        entry_detalle = tk.Entry(ventana, textvariable=detalle)
        entry_detalle.grid(row=1, column=1, padx=10, pady=5)
    
        def confirmar():
            nonlocal resultado
            if nombre.get().strip() and detalle.get().strip():
                if metodo == "paypal":
                    resultado = f"Nombre: {nombre.get().strip()}, Correo: {detalle.get().strip()}"
                else:
                    resultado = f"Nombre: {nombre.get().strip()}, Tarjeta: {detalle.get().strip()}"
                
                # Mostrar un mensaje si el dato es incorrecto
                if metodo == "paypal" and "@" not in detalle.get().strip():
                    messagebox.showerror("Error", "El correo de PayPal es incorrecto. Por favor, corríjalo.")
                elif metodo != "paypal" and len(detalle.get().strip()) < 13:
                    messagebox.showerror("Error", "El número de tarjeta es incorrecto. Debe tener al menos 13 caracteres.")
                else:
                    ventana.destroy()  # Si todo es correcto, cerramos la ventana
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios. Por favor, complete los datos.")

        btn_confirmar = tk.Button(ventana, text="Confirmar", command=confirmar)
        btn_confirmar.grid(row=2, columnspan=2, pady=10)
    
        # Hacer la ventana modal y esperar
        ventana.grab_set()
        ventana.wait_window()
    
        return resultado

    def volver(self):
        self.root.destroy()
        open_cine_screen()

# Pantalla de Museo
class MuseoScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("TicketMaster - Museo")
        self.root.geometry("500x400")

        self.label_museo = tk.Label(root, text="Seleccione un museo:")
        self.label_museo.pack(pady=10)

        self.museos = [
            "Elija una opción",
            "Museo de Louvre, París",
            "Museo Metropolitano de Nueva York",
            "Museo Vaticano",
            "Museo Nacional de Antropología, CDMX",
            "Museu Nacional d'Art de Catalunya"
        ]
        self.combo_museo = tk.StringVar(root)
        self.combo_museo.set(self.museos[0])
        self.dropdown_museo = tk.OptionMenu(root, self.combo_museo, *self.museos)
        self.dropdown_museo.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def continuar(self):
        museo_seleccionado = self.combo_museo.get()
        if museo_seleccionado == "Elija una opción":
            messagebox.showerror("Error", "Debes seleccionar un museo.")
            return

        self.root.destroy()
        open_museo_detalle(museo_seleccionado)

    def volver(self):
        self.root.destroy()
        open_main_menu()

class MuseoDetalleScreen:
    def __init__(self, root, museo):
        self.root = root
        self.root.title("TicketMaster - Detalles del Museo")
        self.root.geometry("600x500")

        self.museo = museo
        self.capacidad = self.obtener_capacidad(museo)
        self.restricciones = self.obtener_restricciones(museo)

        self.label_museo = tk.Label(root, text=f"Museo: {museo}")
        self.label_museo.pack(pady=10)
        self.label_capacidad = tk.Label(root, text=f"Capacidad: {self.capacidad} personas/día")
        self.label_capacidad.pack(pady=10)

        # Campos de entrada
        self.label_fecha = tk.Label(root, text="Fecha (dd/mm/aaaa):")
        self.label_fecha.pack(pady=10)
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.pack(pady=10)

        self.label_horario = tk.Label(root, text="Horario:")
        self.label_horario.pack(pady=10)
        self.horarios = [
            "Elija una opción",
            "09:00 - 12:00",
            "13:00 - 16:00",
            "17:00 - 20:00"
        ]
        self.combo_horario = tk.StringVar(root)
        self.combo_horario.set(self.horarios[0])
        self.dropdown_horario = tk.OptionMenu(root, self.combo_horario, *self.horarios)
        self.dropdown_horario.pack(pady=10)

        self.label_boletos = tk.Label(root, text="Cantidad de boletos (1-5):")
        self.label_boletos.pack(pady=10)
        self.entry_boletos = tk.Entry(root)
        self.entry_boletos.pack(pady=10)

        self.button_continuar = tk.Button(root, text="Continuar", command=self.continuar)
        self.button_continuar.pack(pady=20)
        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=10)

    def obtener_capacidad(self, museo):
        capacidades = {
            "Museo de Louvre, París": 5000,
            "Museo Metropolitano de Nueva York": 3000,
            "Museo Vaticano": 2000,
            "Museo Nacional de Antropología, CDMX": 1500,
            "Museu Nacional d'Art de Catalunya": 1000
        }
        return capacidades.get(museo, 0)

    def obtener_restricciones(self, museo):
        restricciones = {
            "Museo de Louvre, París": "No se permite la entrada con mochilas grandes ni cámaras profesionales.",
            "Museo Metropolitano de Nueva York": "No se permite la entrada con alimentos o bebidas.",
            "Museo Vaticano": "Vestimenta apropiada requerida (sin ropa corta o escotada).",
            "Museo Nacional de Antropología, CDMX": "No se permiten cámaras en ciertas exhibiciones.",
            "Museu Nacional d'Art de Catalunya": "No se permite la entrada con grandes bolsas ni cámaras de video."
        }
        return restricciones.get(museo, "")

    def continuar(self):
        try:
            fecha = self.entry_fecha.get()
            dia, mes, anio = map(int, fecha.split('/'))
            
            if not (1 <= mes <= 12):
                raise ValueError("Mes inválido")
            
            dias_mes = [31,29 if es_bisiesto(anio) else 28,31,30,31,30,31,31,30,31,30,31]
            if not (1 <= dia <= dias_mes[mes-1]):
                raise ValueError("Día inválido")
            
            if es_dia_festivo(dia, mes, anio):
                messagebox.showwarning("Día festivo", 
                    "No se permiten compras en días festivos.\n\nDías festivos en México:\n"
                    "- 1 Enero: Año Nuevo\n- 3 Feb: Día Constitución\n- 17 Mar: Natalicio Benito Juárez\n"
                    "- 17-18 Abr: Jueves/Viernes Santo\n- 1 Mayo: Día Trabajo\n- 16 Sep: Independencia\n"
                    "- 17 Nov: Revolución\n- 25 Dic: Navidad")
                return

        except Exception as e:
            messagebox.showerror("Error", f"Fecha inválida: {str(e)}")
            return

        if (self.combo_horario.get() == "Elija una opción"):
            messagebox.showerror("Error", "Seleccione un horario válido")
            return

        try:
            boletos = int(self.entry_boletos.get())
            if not (1 <= boletos <= 5):
                raise ValueError("Máximo 5 boletos")
            if boletos > self.capacidad:
                raise ValueError(f"Excede capacidad máxima ({self.capacidad})")
        except Exception as e:
            messagebox.showerror("Error", f"Cantidad inválida: {str(e)}")
            return

        # Calcular total
        total = 20.00 * boletos

        # Construir resumen
        resumen = f"""--- Resumen de la Compra ---
Museo: {self.museo}
Fecha: {fecha}
Horario: {self.combo_horario.get()}
Cantidad de boletos: {boletos}
Precio total: ${total:.2f}
Restricciones: {self.restricciones}"""

        # Método de pago
        metodo_pago = self.solicitar_metodo_pago()
        if not metodo_pago:
            return

        # Datos de pago
        datos_pago = self.solicitar_datos_pago(metodo_pago)
        if not datos_pago:
            return

        resumen += f"\nMétodo de pago: {metodo_pago}"
        resumen += f"\nDatos de pago: {datos_pago}"

        # Mostrar resumen
        self.root.destroy()
        root = tk.Tk()
        ResumenScreen(root, resumen)

    def solicitar_metodo_pago(self):
        # Mismo método que en TeatroDetalleScreen
        ventana = tk.Toplevel()
        ventana.title("Método de Pago")
        metodo = tk.StringVar(value="tarjeta de crédito")
        
        tk.Label(ventana, text="Seleccione método de pago:").pack(pady=10)
        opciones = [
            ("Tarjeta de Crédito", "tarjeta de crédito"),
            ("Tarjeta de Débito", "tarjeta de débito"),
            ("PayPal", "paypal")
        ]
        
        for texto, valor in opciones:
            tk.Radiobutton(ventana, text=texto, variable=metodo, value=valor).pack()
        
        confirmado = [False]
        def confirmar():
            confirmado[0] = True
            ventana.destroy()
        
        tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        ventana.wait_window()
        
        return metodo.get() if confirmado[0] else None

    def solicitar_datos_pago(self, metodo):
        # Mismo método que en TeatroDetalleScreen
        ventana = tk.Toplevel(self.root)
        ventana.title("Datos de Pago")
        ventana.geometry("300x150")
    
        nombre = tk.StringVar()
        detalle = tk.StringVar()
        resultado = None
    
        tk.Label(ventana, text="Nombre del titular:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(ventana, textvariable=nombre)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    
        etiqueta = "Correo de PayPal:" if metodo == "paypal" else "Número de tarjeta:"
        tk.Label(ventana, text=etiqueta).grid(row=1, column=0, padx=10, pady=5)
        entry_detalle = tk.Entry(ventana, textvariable=detalle)
        entry_detalle.grid(row=1, column=1, padx=10, pady=5)
    
        def confirmar():
            nonlocal resultado
            if nombre.get().strip() and detalle.get().strip():
                if metodo == "paypal" and "@" not in detalle.get().strip():
                    messagebox.showerror("Error", "Correo PayPal inválido")
                elif metodo != "paypal" and len(detalle.get().strip()) < 13:
                    messagebox.showerror("Error", "Tarjeta debe tener 13+ dígitos")
                else:
                    resultado = f"Nombre: {nombre.get().strip()}, "
                    resultado += "Correo: " if metodo == "paypal" else "Tarjeta: "
                    resultado += detalle.get().strip()
                    ventana.destroy()
            else:
                messagebox.showerror("Error", "Complete todos los campos")
    
        tk.Button(ventana, text="Confirmar", command=confirmar).grid(row=2, columnspan=2, pady=10)
        ventana.grab_set()
        ventana.wait_window()
        return resultado

    def volver(self):
        self.root.destroy()
        open_museo_screen()

class ResumenScreen:
    def __init__(self, root, resumen):
        self.root = root
        self.root.title("Resumen de Compra")
        self.root.geometry("400x400")
        
        self.label_resumen = tk.Label(root, text=resumen, justify=tk.LEFT)
        self.label_resumen.pack(pady=10)

        self.button_volver = tk.Button(root, text="Volver", command=self.volver)
        self.button_volver.pack(pady=20)

    def volver(self):
        self.root.destroy()
        # Función para abrir la pantalla principal nuevamente (cine)
        open_main_menu()
# Funciones para navegación
def open_login_screen():
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()

def open_register_screen():
    root = tk.Tk()
    RegisterScreen(root)
    root.mainloop()

def open_main_menu():
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()

def open_cine_screen():
    root = tk.Tk()
    cine_screen = CineScreen(root)
    root.mainloop()

def open_cine_detalle(cine):
    root = tk.Tk()
    CineDetalleScreen(root, cine)
    root.mainloop()

def open_teatro_screen():
    root = tk.Tk()
    TeatroScreen(root)
    root.mainloop()

def open_teatro_detalle(teatro):
    root = tk.Tk()
    TeatroDetalleScreen(root, teatro)
    root.mainloop()

def open_museo_screen():
    root = tk.Tk()
    MuseoScreen(root)
    root.mainloop()

def open_museo_detalle(museo):
    root = tk.Tk()
    MuseoDetalleScreen(root, museo)
    root.mainloop()

# Inicio de la aplicación
if __name__ == "__main__":
    open_login_screen()