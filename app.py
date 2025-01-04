from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from forms import JobApplicationForm, LoginForm, SignupForm
from models import JobApplication, User
from extensions import db

app = Flask(__name__)
bycrypt = Bcrypt(app)
csrf = CSRFProtect(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up! Please log in.', 'success')
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            print(f"User {user.username} logged in.") 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/form', methods=['GET','POST'])
@login_required
def form():
    form = JobApplicationForm()
    if form.validate_on_submit():
        print("Form submitted successfully.")
        print("Data:", form.data)

        application = JobApplication(
            date_submitted=form.date_submitted.data,
            due_date=form.due_date.data,
            follow_up_date=form.follow_up_date.data,
            company=form.company.data,
            contact=form.contact.data,
            position_title=form.position_title.data,
            status=form.status.data,
            cv_submitted=form.cv_submitted.data,
            cover_letter_submitted=form.cover_letter_submitted.data,
            follow_up_sent=form.follow_up_sent.data,
            follow_up_message=form.follow_up_message.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        # Add the new data to the database
        db.session.add(application)
        db.session.commit()
        flash('Job application submitted successfully!', 'success')
        # Redirect to the dashboard
        return redirect(url_for('dashboard'))
    else:
        print("Form validation failed.")
        print("Errors:", form.errors)
        flash('Form validation failed. Please check your inputs.', 'danger')
    return render_template('form.html', form=form)

class DeleteForm(FlaskForm):
    csrf_token = HiddenField()

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    print(f"User authenticated: {current_user.is_authenticated}")
    all_applications = JobApplication.query.filter_by(user_id=current_user.id).all()

    filtered_applications = []
    for application in all_applications:
        if request.args.get('status') and request.args.get('status') != application.status:
            continue
        if request.args.get('company') and request.args.get('company').lower() not in application.company.lower():
            continue
        if request.args.get('due_before') and application.due_date:
            due_before = datetime.strptime(request.args.get('due_before'), "%d-%m-%Y")
            if application.due_date > due_before:
                continue
            filtered_applications.append(application)
    
    # Add priority flag
    for app in filtered_applications:
        if app.due_date and app.due_date < datetime.utcnow() + timedelta(days=2):
            app.priority = 'high'  # Nearly due
        elif app.status == 'Offer Received':
            app.priority = 'completed'
        else:
            app.priority = 'normal'
    
    application_form = JobApplicationForm()
    delete_form = DeleteForm()

    return render_template(
        'dashboard.html', 
        applications=filtered_applications or all_applications,
        application_form=application_form,
        delete_form=delete_form)

@app.route('/application/<int:application_id>', methods=['GET'])
@login_required
def view_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    if application.user_id != current_user.id:
        flash("You are not authorized to view this application.", "danger")
        return redirect(url_for('dashboard'))
    return render_template('view_application.html', application=application)

@app.route('/application/<int:application_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    print(f"Editing application: {application}") 

    if application.user_id != current_user.id:
        flash("You are not authorised to edit this application.", "danger")
        return redirect(url_for('dashboard'))

    form = JobApplicationForm(obj=application)

    if form.validate_on_submit():
        print(f"Form data: {form.data}")
        application.date_submitted = form.date_submitted.data
        application.due_date = form.due_date.data
        application.follow_up_date = form.follow_up_date.data
        application.company = form.company.data
        application.contact = form.contact.data
        application.position_title = form.position_title.data
        application.status = form.status.data
        application.cv_submitted = form.cv_submitted.data
        application.cover_letter_submitted = form.cover_letter_submitted.data
        application.follow_up_sent = form.follow_up_sent.data
        application.follow_up_message = form.follow_up_message.data
        application.notes = form.notes.data

        db.session.commit()
        flash('Job application updated successfully!', 'success')
        print(f"Updated application: {application}")
        return redirect(url_for('dashboard'))
    
    return render_template('edit_application.html', form=form)

@app.route('/application/<int:application_id>/delete', methods=['POST'])
@login_required
def delete_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    if application.user_id != current_user.id:
        flash("You are not authorized to delete this application.", "danger")
        return redirect(url_for('dashboard'))

    db.session.delete(application)
    db.session.commit()
    flash('Job application deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)