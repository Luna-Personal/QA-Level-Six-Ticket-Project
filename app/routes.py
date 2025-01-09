from flask import render_template, url_for, flash, redirect, request, Blueprint  # Import necessary modules from Flask
from app import db, bcrypt  # Import db and bcrypt instances from the app package
from app.forms import RegistrationForm, LoginForm, TicketForm  # Import forms from the forms module
from app.models import User, Ticket  # Import models from the models module
from flask_login import login_user, current_user, logout_user, login_required  # Import Flask-Login functions

# Define the main blueprint
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    """
    Home route to display all tickets.
    """
    tickets = Ticket.query.all()  # Query all tickets from the database
    return render_template('index.html', tickets=tickets)  # Render the home page template with the tickets

@main.route("/register", methods=['GET', 'POST'])
def register():
    """
    Registration route to create a new user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Redirect authenticated users to the home page
    form = RegistrationForm()  # Create an instance of the registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Create a new user
        db.session.add(user)  # Add the user to the database session
        db.session.commit()  # Commit the session to save the user
        flash('Your account has been created!', 'success')  # Flash a success message
        return redirect(url_for('main.login'))  # Redirect to the login page
    return render_template('register.html', title='Register', form=form)  # Render the registration page template

@main.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login route to authenticate a user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Redirect authenticated users to the home page
    form = LoginForm()  # Create an instance of the login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Query the user by email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Check the password
            login_user(user, remember=form.remember.data)  # Log in the user
            next_page = request.args.get('next')  # Get the next page from the request arguments
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # Redirect to the next page or home
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # Flash an error message
    return render_template('login.html', title='Login', form=form)  # Render the login page template

@main.route("/logout")
def logout():
    """
    Logout route to log out the current user.
    """
    logout_user()  # Log out the user
    return redirect(url_for('main.home'))  # Redirect to the home page

@main.route("/ticket/new", methods=['GET', 'POST'])
@login_required  # Require login to access this route
def new_ticket():
    """
    Route to create a new ticket.
    """
    form = TicketForm()  # Create an instance of the ticket form
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, content=form.content.data, author=current_user)  # Create a new ticket
        db.session.add(ticket)  # Add the ticket to the database session
        db.session.commit()  # Commit the session to save the ticket
        flash('Your ticket has been created!', 'success')  # Flash a success message
        return redirect(url_for('main.home'))  # Redirect to the home page
    return render_template('ticket_form.html', title='New Ticket', form=form, legend='New Ticket')  # Render the ticket form template