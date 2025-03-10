# models.py
from extensions import db
from flask_login import UserMixin  # Añadir UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Cine, Teatro, Museo
    date = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='tickets')
    event = db.relationship('Event', backref='tickets')

class CineTicket(db.Model):
    __tablename__ = 'cine_ticket'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cine = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    pelicula = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    seccion = db.Column(db.String(50), nullable=False)
    cantidad_boletos = db.Column(db.Integer, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    numero_tarjeta = db.Column(db.String(50))
    nombre_pago = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asientos = db.Column(db.String(255), nullable=False)  # Nueva columna para almacenar los asientos

    user = db.relationship('User', backref=db.backref('cine_tickets', lazy=True))

    def __repr__(self):
        return f'<CineTicket {self.id}>'

class TeatroTicket(db.Model):
    __tablename__ = 'teatro_ticket'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teatro = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    obra = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    seccion = db.Column(db.String(50), nullable=False)
    cantidad_boletos = db.Column(db.Integer, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    numero_tarjeta = db.Column(db.String(50))  # ⚠️ No recomendado almacenar tarjetas
    nombre_pago = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('teatro_tickets', lazy=True))

    def __repr__(self):
        return f'<TeatroTicket {self.id}>'

class MuseoTicket(db.Model):
    __tablename__ = 'museo_ticket'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    museo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    cantidad_boletos = db.Column(db.Integer, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    numero_tarjeta = db.Column(db.String(50))  # ⚠️ No recomendado almacenar tarjetas
    nombre_pago = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('museo_tickets', lazy=True))

    def __repr__(self):
        return f'<MuseoTicket {self.id}>'
