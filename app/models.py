# Importing packages
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
# Creates a function to reload the user stored in the session
def load_user(user_id):
    return User.query.get(int(user_id))


# Creates a User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    tickets = db.relationship('Ticket', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Creates a Ticket Class
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Ticket('{self.title}', '{self.date_posted}')"


# Creates a Department Class
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tickets = db.relationship('TicketAssignment', backref='department', lazy=True)

    def __repr__(self):
        return f"Department('{self.name}')"


# Creates a Ticket Assignment Class
class TicketAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"TicketAssignment('{self.ticket_id}', '{self.department_id}', '{self.assigned_date}')"
