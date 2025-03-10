import random
import string
import json 

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extensions import db
from models import User, CineTicket, TeatroTicket, MuseoTicket  # Importar User desde models
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/ticketmaster_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'  # Necesario para manejar sesiones de usuario

db.init_app(app)

from models import  CineTicket
# Inicializar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Si el usuario no está autenticado, lo redirige al login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_ticket_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cine')
def cine():
    return render_template('cine.html')



@app.route('/teatro')
def teatro():
    return render_template('teatro.html')

@app.route('/museo')
def museo():
    return render_template('museo.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validación de nombre de usuario
        username_pattern = r'^[A-Za-z]{4}\d{6}[A-Za-z][A-Za-z]{2}[A-Za-z0-9]{3}[A-Z]{2}\d{2}$'
        if not re.match(username_pattern, username):
            flash('''El nombre de usuario debe seguir el formato:
            4 letras + 6 números + 1 letra + 2 letras + 3 letras/números + 2 letras de estado + 2 números''', 'error')
            return redirect(url_for('register'))
        
        # Validación de contraseña
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!])[A-Za-z\d@#$%&!]{8}$'
        if not re.match(password_pattern, password):
            flash('''La contraseña debe tener exactamente 8 caracteres y contener:
            - Al menos una mayúscula
            - Al menos una minúscula
            - Al menos un número
            - Al menos un carácter especial (@, #, $, %, &, !)''', 'error')
            return redirect(url_for('register'))
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya está registrado', 'error')
            return redirect(url_for('register'))
        
        # Crear nuevo usuario sin encriptar la contraseña
        new_user = User(
            username=username,
            password=password  # Contraseña sin encriptar
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro exitoso! Por favor inicia sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/procesar-compra', methods=['GET', 'POST'])
@login_required
def procesar_compra():
    if request.method == 'POST':
        cine = request.form['cine']
        fecha = request.form['fecha']
        pelicula = request.form['pelicula']
        horario = request.form['horario']
        seccion = request.form['seccion']
        cantidad_boletos = request.form['cantidad']
        metodo_pago = request.form['metodoPago']
        numero_tarjeta = request.form.get('numeroTarjeta', '')
        nombre_pago = request.form.get('nombrePago', '')
        
       # Obtener los asientos seleccionados
        asientos_json = request.form.get('asientos')
        if not asientos_json:
            flash('Debes seleccionar al menos un asiento', 'error')
            return redirect(url_for('procesar_compra'))
        
        try:
            asientos = json.loads(asientos_json)  # <-- Indentación correcta
        except json.JSONDecodeError:  # <-- Except al mismo nivel que el try
            flash('Error en los datos de los asientos', 'error')
            return redirect(url_for('procesar_compra'))  # <-- Indentación correcta
    
        asientos_str = ", ".join(asientos)

        # Crear una nueva compra en la tabla CineTicket
        ticket = CineTicket(
            cine=cine,
            fecha=fecha,
            pelicula=pelicula,
            horario=horario,
            seccion=seccion,
            cantidad_boletos=cantidad_boletos,
            metodo_pago=metodo_pago,
            numero_tarjeta=numero_tarjeta,
            nombre_pago=nombre_pago,
            user_id=current_user.id,
            asientos=asientos_str  # Guardar los asientos como una cadena
        )
        
        db.session.add(ticket)
        db.session.commit()

        flash('Compra procesada exitosamente', 'success')
        return redirect(url_for('resumen_compra', ticket_id=ticket.id))  # Redirigir a una página de éxito o al dashboard

    return render_template('cine.html')


@app.route('/resumen_compra/<int:ticket_id>')
def resumen_compra(ticket_id):
    # Obtener el ticket utilizando el ticket_id
    ticket = CineTicket.query.filter_by(id=ticket_id).first()

    # Si el ticket no se encuentra, redirigir o mostrar mensaje de error
    if ticket is None:
        flash('El ticket no existe', 'danger')
        return redirect(url_for('dashboard'))

    # Si el ticket existe, renderizar el resumen
    return render_template('resumen_compra.html', ticket=ticket)

@app.route('/procesar-compra2', methods=['GET', 'POST'])
@login_required
def procesar_compra2():
    if request.method == 'POST':
        teatro = request.form['teatro']
        fecha = request.form['fecha']
        obra = request.form['obra']
        horario = request.form['horario']
        seccion = request.form['seccion']
        cantidad_boletos = request.form['cantidad']
        metodo_pago = request.form['metodoPago']
        numero_tarjeta = request.form.get('numeroTarjeta', '')
        nombre_pago = request.form.get('nombrePago', '')

        # Crear una nueva compra en la tabla TeatroTicket
        ticket = TeatroTicket(
            teatro=teatro,
            fecha=fecha,
            obra=obra,
            horario=horario,
            seccion=seccion,
            cantidad_boletos=cantidad_boletos,
            metodo_pago=metodo_pago,
            numero_tarjeta=numero_tarjeta,
            nombre_pago=nombre_pago,
            user_id=current_user.id
        )
        
        db.session.add(ticket)
        db.session.commit()

        flash('Compra de teatro procesada exitosamente', 'success')
        return redirect(url_for('resumen_compra_teatro', ticket_id=ticket.id))  

    return render_template('teatro.html')  # Asegúrate de tener una plantilla para teatro

@app.route('/resumen_compra_teatro/<int:ticket_id>')
def resumen_compra_teatro(ticket_id):
    # Obtener el ticket utilizando el ticket_id
    ticket = TeatroTicket.query.filter_by(id=ticket_id).first()

    if ticket is None:
        flash('El ticket no existe', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('resumen_compra_teatro.html', ticket=ticket)

@app.route('/procesar-compra3', methods=['GET', 'POST'])
@login_required
def procesar_compra_museo():
    if request.method == 'POST':
        museo = request.form['museo']
        fecha = request.form['fecha']
        horario = request.form['horario']
        cantidad_boletos = request.form['cantidad']
        metodo_pago = request.form['metodoPago']
        numero_tarjeta = request.form.get('numeroTarjeta', '')
        nombre_pago = request.form.get('nombrePago', '')

        # Crear una nueva compra en la tabla MuseoTicket
        ticket = MuseoTicket(
            museo=museo,
            fecha=fecha,
            horario=horario,
            cantidad_boletos=cantidad_boletos,
            metodo_pago=metodo_pago,
            numero_tarjeta=numero_tarjeta,
            nombre_pago=nombre_pago,
            user_id=current_user.id
        )
        
        db.session.add(ticket)
        db.session.commit()

        flash('Compra de museo procesada exitosamente', 'success')
        return redirect(url_for('resumen_compra_museo', ticket_id=ticket.id))  

    return render_template('museo.html')  # Asegúrate de tener una plantilla para museo

@app.route('/resumen_compra_museo/<int:ticket_id>')
def resumen_compra_museo(ticket_id):
    # Obtener el ticket utilizando el ticket_id
    ticket = MuseoTicket.query.filter_by(id=ticket_id).first()

    if ticket is None:
        flash('El ticket no existe', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('resumen_compra_museo.html', ticket=ticket)


if __name__ == '__main__':
    with app.app_context():  # Activa el contexto de la aplicación
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
