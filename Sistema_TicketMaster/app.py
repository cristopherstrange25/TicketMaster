import random
import string
import json 
import qrcode
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extensions import db
from models import User, CineTicket, TeatroTicket, MuseoTicket  # Importar User desde models
from werkzeug.security import generate_password_hash
import re, base64, io

import unittest
from flask_testing import TestCase
from werkzeug.security import check_password_hash
import json
from flask_login import (
    LoginManager, 
    UserMixin, 
    login_user, 
    logout_user, 
    login_required, 
    current_user
)
from flask_testing import TestCase  # <-- Nuevo

# Componentes de seguridad
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'pdf')

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import uploader


# Configuración con tus credenciales
cloudinary.config(
  cloud_name = "dcndmmy9m",
  api_key = "***oculto***",
  api_secret = "***oculto***"
)


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


# En tu aplicación Flask
from twilio.rest import Client



# Configura tus credenciales de Twilio
  cloud_name = "dcndmmy9m",
  api_key = "***oculto***",
  api_secret = "***oculto***"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Clase base para pruebas
class TestBase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Métodos auxiliares comunes
    def _registrar_usuario(self):
        self.client.post('/register', data={
            'username': 'XXXX111111XXXXXXXX11',
            'password': 'Abc123$%'
        })
        self.client.post('/login', data={
            'username': 'XXXX111111XXXXXXXX11',
            'password': 'Abc123$%'
        })

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    verificado = False
    username = ""
    nombre = ""
    correo = ""

    if request.method == 'POST':
        if 'verificar' in request.form:
            username = request.form.get('username2')
            nombre = request.form.get('nombre2')
            correo = request.form.get('correo2')

            user = User.query.filter_by(username=username, nombre=nombre, correo=correo).first()

            if user:
                session['verificado'] = True
                session['username'] = username
                session['nombre'] = nombre
                session['correo'] = correo
                flash('Identidad verificada. Introduce tu nueva contraseña.', 'success')
                return redirect(url_for('recuperar'))
            else:
                flash('Datos incorrectos. Verifica tu CURP, nombre y correo.', 'error')

        elif 'cambiar' in request.form:
            if not session.get('verificado'):
                flash('Primero verifica tu identidad.', 'error')
                return redirect(url_for('recuperar'))

            username = session.get('username')
            nueva_contrasena = request.form.get('nueva_contrasena2')

            password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!])[A-Za-z\d@#$%&!]{8}$'
            if not re.match(password_pattern, nueva_contrasena):
                flash('La contraseña debe tener 8 caracteres, incluyendo mayúsculas, minúsculas, números y símbolos (@#$%&!)', 'error')
                return redirect(url_for('recuperar'))

            user = User.query.filter_by(username=username).first()
            if user:
                user.password = generate_password_hash(nueva_contrasena)
                db.session.commit()
                session.clear()
                flash('Contraseña actualizada correctamente. Inicia sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error al actualizar la contraseña.', 'error')

    verificado = session.get('verificado', False)
    username = session.get('username', "")
    nombre = session.get('nombre', "")
    correo = session.get('correo', "")

    return render_template('recuperar.html', verificado=verificado, username=username, nombre=nombre, correo=correo)

def generate_qr_code(ticket_data, ticket_id):
    # Crear directorio si no existe
        qr_dir = os.path.join(os.getcwd(), 'static', 'qr_codes')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)
    
    # Generar nombre único de archivo
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"qr_{ticket_id}_{timestamp}.png"
        filepath = os.path.join(qr_dir, filename)
    
    # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    
            # Personalizar contenido según tipo de ticket
        if 'pelicula' in ticket_data:  # Cine
            qr_content = f"""Cine:
            Película: {ticket_data['pelicula']}
            Fecha: {ticket_data['fecha']}
            Asientos: {ticket_data['asientos']}"""
        
        elif 'obra' in ticket_data:  # Teatro
            qr_content = f"""Teatro:
            Obra: {ticket_data['obra']}
            Fecha: {ticket_data['fecha']}
            Sección: {ticket_data['sección']}"""
        
        elif 'museo' in ticket_data:  # Museo
            qr_content = f"""Museo:
            {ticket_data['museo']}
            Fecha: {ticket_data['fecha']}
            Visitantes: {ticket_data['visitantes']}"""
    
        qr.add_data(qr_content)
        qr.make(fit=True)
    
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
    
        return f"static/qr_codes/{filename}"


    

# Pruebas de autenticación
class TestAuthRoutes(TestBase):
    def test_registro_valido(self):
        response = self.client.post('/register', data={
            'username': 'XXXX111111XXXXXXXX12',
            'password': 'Abc123$%'
        }, follow_redirects=True)
        self.assertIn(b'Registro exitoso', response.data)
    
    def test_login_valido(self):
        self.client.post('/register', data={'username': 'XXXX111111XXXXXXXX12', 'password': 'Abc123$%'})
        response = self.client.post('/login', data={
            'username': 'XXXX111111XXXXXXXX12',
            'password': 'Abc123$%'
        })
        self.assertEqual(response.status_code, 302)

    def test_registro_usuario_invalido(self):
        response = self.client.post('/register', data={
            'username': 'user_invalido',
            'password': 'Aa1@aaaa'
        })
        self.assertIn(b'formato', response.data)
    
    def test_login_password_invalido(self):
        self.client.post('/register', data={'username': 'TEST1234abcdMX99', 'password': 'Aa1@aaaa'})
        response = self.client.post('/login', data={
            'username': 'TEST1234abcdMX99',
            'password': 'password_incorrecto'
        })
        self.assertIn(b'incorrectas', response.data)

# Pruebas de Cine
class TestCineRoutes(TestBase):
    def _data_valida_cine(self):
        return {
            'cine': 'Cinepolis',
            'fecha': '2024-12-31',
            'pelicula': 'Avengers',
            'horario': '21:00',
            'seccion': 'VIP',
            'cantidad': '2',
            'metodoPago': 'tarjeta',
            'numeroTarjeta': '123212312345',
            'nombrePago': 'Juan Perez',
            'asientos': '["A1", "A2"]'
        }


    def test_compra_valida_con_asientos(self):
        self._registrar_usuario()
        response = self.client.post('/resumen_compra', data=self._data_valida_cine())
        self.assertEqual(CineTicket.query.count(), 1)
    

    def test_compra_sin_asientos(self):
        self._registrar_usuario()
        data = self._data_valida_cine()
        del data['asientos']
        response = self.client.post('/procesar-compra', data=data)
        self.assertIn(b'seleccionar', response.data)
    
    def test_compra_fecha_pasada(self):
        self._registrar_usuario()
        data = self._data_valida_cine()
        data['fecha'] = '2000-01-01'
        response = self.client.post('/procesar-compra', data=data)
        self.assertIn(b'fecha', response.data)

# Pruebas de Teatro
class TestTeatroRoutes(TestBase):
    def _data_valida_teatro(self):
        return {
            'teatro': 'Teatro Colón',
            'fecha': '2024-12-31',
            'obra': 'Romeo y Julieta',
            'horario': '21:00',
            'seccion': 'VIP',
            'cantidad': '2',
            'metodoPago': 'tarjeta',
            'numeroTarjeta': '4111111111111111',
            'nombrePago': 'Juan Perez'
        }

    def test_compra_teatro_valida(self):
        self._registrar_usuario()
        response = self.client.post('/procesar-compra2', data=self._data_valida_teatro())
        self.assertEqual(TeatroTicket.query.count(), 1)
    

    def test_compra_teatro_sin_obra(self):
        self._registrar_usuario()
        data = self._data_valida_teatro()
        del data['obra']
        response = self.client.post('/procesar-compra2', data=data)
        self.assertIn(b'requerido', response.data)
    
    def test_compra_teatro_capacidad_excedida(self):
        self._registrar_usuario()
        data = self._data_valida_teatro()
        data['cantidad'] = '11'
        response = self.client.post('/procesar-compra2', data=data)
        self.assertIn('máximo', response.data.decode('utf-8'))

# Pruebas de Museo
class TestMuseoRoutes(TestBase):
    def _data_valida_museo(self):
        return {
            'museo': 'Museo Louvre',
            'fecha': '2024-12-31',
            'horario': '09:00 - 12:00',
            'cantidad': '2',
            'metodoPago': 'tarjeta',
            'numeroTarjeta': '4111111111111111',
            'nombrePago': 'Juan Perez'
        }

    def test_compra_museo_valida(self):
        self._registrar_usuario()
        response = self.client.post('/procesar-compra3', data=self._data_valida_museo())
        self.assertEqual(MuseoTicket.query.count(), 1)
    

    def test_compra_museo_sin_horario(self):
        self._registrar_usuario()
        data = self._data_valida_museo()
        del data['horario']
        response = self.client.post('/procesar-compra3', data=data)
        self.assertIn(b'requerido', response.data)
    
    def test_compra_museo_exceso_boletos(self):
        self._registrar_usuario()
        data = self._data_valida_museo()
        data['cantidad'] = '6'
        response = self.client.post('/procesar-compra3', data=data)
        self.assertIn('máximo', response.data.decode('utf-8'))



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

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'error': 'No se ha proporcionado ningún archivo PDF'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'}), 400

        filename = 'ticket.pdf'  # O utiliza el nombre del archivo original

        upload_result = cloudinary.uploader.upload(
        file,
        resource_type="auto",  # <--- CAMBIO CLAVE
        folder="tickets-pdf/",
        public_id=f"ticket_{filename}",
        use_filename=True,
        unique_filename=False,
        overwrite=True,
        invalidate=True
        )



        return jsonify({
            'success': True, 
            'url': upload_result['secure_url']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/enviar-whatsapp', methods=['POST'])
def enviar_whatsapp():
    try:
        data = request.json
        phone_number = data.get('phone')
        message_body = data.get('message')
        media_url = data.get('media_url')  # Espera la URL del PDF subido
        
        # Depuración
        print("Número de teléfono:", phone_number)
        print("Mensaje:", message_body)
        print("Media URL:", media_url)
        
        # Validación del número de teléfono con formato internacional
        if not re.match(r'^\+\d{1,15}$', phone_number):
            return jsonify({'success': False, 'error': 'Formato de número inválido'}), 400
        
        message_data = {
            'from_': TWILIO_WHATSAPP_NUMBER,
            'to': f'whatsapp:{phone_number}',
            'body': message_body
        }
        
        
        
        # Enviar el mensaje a través de Twilio
        message = client.messages.create(**message_data)
        print("Mensaje enviado. SID:", message.sid)
        return jsonify({'success': True, 'message_id': message.sid})
        
    except Exception as e:
        print("Error al enviar:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


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
        user = User.query.filter_by(username=username).first()  # Solo buscar por usuario
        
        # Verificar contraseña con el hash almacenado
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        username = request.form['username']
        password = request.form['password']

        # Validación CURP
        username_pattern = r'^[A-Za-z]{4}\d{6}[A-Za-z][A-Za-z]{2}[A-Za-z0-9]{3}[A-Z]{2}\d{2}$'
        if not re.match(username_pattern, username):
            flash('''El CURP debe seguir el formato:
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

        # Validar que username y correo no existan
        if User.query.filter_by(username=username).first():
            flash('El CURP ya está registrado', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado', 'error')
            return redirect(url_for('register'))

        # Crear usuario
        hashed_password = generate_password_hash(password)
        new_user = User(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            username=username,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Por favor inicia sesión.', 'success')
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

def generate_qr_code_blob(qr_data, ticket_id):
    # Opcional: Puedes incluir ticket_id o cualquier información adicional en qr_data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen en un buffer en memoria
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.read()  # Retorna los bytes de la imagen

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
            asientos = json.loads(asientos_json)
        except json.JSONDecodeError:
            flash('Error en los datos de los asientos', 'error')
            return redirect(url_for('procesar_compra'))
    
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

        try:
            # Datos que deseas incluir en el QR
            qr_data = {
                'pelicula': pelicula,
                'fecha': fecha,
                'horario': horario,
                'asientos': asientos_str
            }
            # Generar el QR como blob (bytes)
            qr_blob = generate_qr_code_blob(qr_data, ticket.id)
            ticket.qr_code = qr_blob
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error generando código QR', 'error')
            return redirect(url_for('procesar_compra'))

        flash('Compra procesada exitosamente', 'success')
        return redirect(url_for('resumen_compra', ticket_id=ticket.id))
    
    return render_template('cine.html')


@app.route('/resumen-compra/<int:ticket_id>')
@login_required
def resumen_compra(ticket_id):
    visible = True
    ticket = CineTicket.query.get_or_404(ticket_id)
    qr_code_b64 = None
    if ticket.qr_code:
        qr_code_b64 = base64.b64encode(ticket.qr_code).decode('utf-8')
    return render_template('resumen_compra.html', ticket=ticket, qr_code_b64=qr_code_b64)


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

        # Crear un ticket sin el QR aún
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
        db.session.commit()  # Necesario para que el ticket tenga un ID

        try:
            qr_data = {
                'obra': obra,
                'fecha': fecha,
                'horario': horario,
                'sección': seccion
            }
            # Generar el QR como blob (bytes)
            qr_blob = generate_qr_code_blob(qr_data, ticket.id)
            ticket.qr_code = qr_blob
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error generando el código QR', 'error')
            return redirect(url_for('procesar_compra2'))

        flash('Compra de teatro procesada exitosamente', 'success')
        return redirect(url_for('resumen_compra_teatro', ticket_id=ticket.id))

    return render_template('teatro.html')


@app.route('/resumen_compra_teatro/<int:ticket_id>')
def resumen_compra_teatro(ticket_id):
    # Obtener el ticket utilizando el ticket_id
    ticket = TeatroTicket.query.get_or_404(ticket_id)

    qr_code_b64 = None
    if ticket.qr_code:
        qr_code_b64 = base64.b64encode(ticket.qr_code).decode('utf-8')
    return render_template('resumen_compra_teatro.html', ticket=ticket, qr_code_b64=qr_code_b64)

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

        try:
            qr_data = {
                'museo': museo,
                'fecha': fecha,
                'horario': horario,
                'visitantes': cantidad_boletos
            }
            #Generar el QR como blob (bytes)
            qr_blob = generate_qr_code_blob(qr_data, ticket.id)
            ticket.qr_code = qr_blob
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error generando código QR', 'error')
        return redirect(url_for('resumen_compra_museo', ticket_id=ticket.id))  
    
    flash('Compra de teatro procesada exitosamente', 'success')
    return render_template('museo.html')  # Asegúrate de tener una plantilla para museo

@app.route('/resumen_compra_museo/<int:ticket_id>')
def resumen_compra_museo(ticket_id):
    # Obtener el ticket utilizando el ticket_id
    ticket = MuseoTicket.query.get_or_404(ticket_id)

    qr_code_b64 = None
    if ticket.qr_code:
        qr_code_b64 = base64.b64encode(ticket.qr_code).decode('utf-8')

    return render_template('resumen_compra_museo.html', ticket=ticket, qr_code_b64=qr_code_b64)


if __name__ == '__main__':
    
    with app.app_context():  # Activa el contexto de la aplicación
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
