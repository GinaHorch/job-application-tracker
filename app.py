from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import HiddenField
from datetime import datetime, timedelta, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, not_
from flask_migrate import Migrate
from dotenv import load_dotenv
from whitenoise import WhiteNoise
from dotenv import load_dotenv
import os
from forms import JobApplicationForm, LoginForm, SignupForm, InterviewStageForm
from models import JobApplication, User, InterviewStage
from extensions import db

load_dotenv()

app = Flask(__name__, static_folder="static")
bycrypt = Bcrypt(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.wsgi_app.add_files("static/", prefix="static/")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', os.getenv('DATABASE_URL', 'sqlite:///default.db'))
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
    elif request.method == 'GET':
        form.username.data = request.args.get('username', '')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("User is already authenticated.")
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Login form submitted. Username: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            print(f"User found: {user.username}")
            if user.check_password(form.password.data):
                print("Password check passed.")
                login_user(user)
                flash('Welcome back, {}!'.format(user.username), 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('No account found with that username. Would you like to sign up?', 'info')
            return redirect(url_for('signup', username=form.username.data))

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
    print(f"User authenticated: {current_user.is_authenticated}")
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
        return redirect(url_for('view_application', application_id=application.id))
    
    if form.errors:
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
    applications = JobApplication.query.filter_by(user_id=current_user.id).all()

    # Apply filters
    status_filter = request.args.get('status')
    company_filter = request.args.get('company')
    due_before_filter = request.args.get('due_before')
    priority_filter = request.args.get('priority')

    if status_filter:
        applications = [app for app in applications if app.status == status_filter]
    if company_filter:
        applications = [app for app in applications if company_filter.lower() in app.company.lower()]
    if due_before_filter:
        try:
            due_before = datetime.strptime(due_before_filter, "%Y-%m-%d").date()
            applications = [app for app in applications if app.due_date and app.due_date <= due_before]
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
    if priority_filter:
        applications = [app for app in applications if app.priority == priority_filter]
    
    # Apply sorting
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')

    def sort_key(x, sort_by):
        value = getattr(x, sort_by, None)
        if isinstance(value, (date, datetime)):
            return (True, value)
        return (value is not None, value)  # This will sort None values last

    if sort_by:
        reverse = order == 'desc'                
        applications = sorted(applications, key=lambda x: sort_key(x, sort_by), reverse=reverse)

    # Filter high priority applications
    high_priority_apps = [app for app in applications if app.priority == 'high']

    # Sort by priority
    sorted_apps = sorted(applications, key=lambda x: x.priority)

    application_form = JobApplicationForm()
    delete_form = DeleteForm()

    rendered_template = render_template(
        'dashboard.html', 
        applications=applications, 
        high_priority_apps=high_priority_apps,
        sorted_apps=sorted_apps,
        application_form=application_form,
        delete_form=delete_form)
    
    # Clear flash messages after rendering
    session.pop('_flashes', None)

    return rendered_template

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
        print("Form validated successfully")

         # Only update fields that the user modified
        if form.date_submitted.data:
            application.date_submitted = form.date_submitted.data
        if form.due_date.data:
            application.due_date = form.due_date.data
        if form.follow_up_date.data:
            application.follow_up_date = form.follow_up_date.data
        if form.company.data:
            application.company = form.company.data
        if form.contact.data:
            application.contact = form.contact.data
        if form.position_title.data:
            application.position_title = form.position_title.data
        if form.status.data:
            application.status = form.status.data
        if form.cv_submitted.data is not None:  # Boolean fields require explicit checks
            application.cv_submitted = form.cv_submitted.data
        if form.cover_letter_submitted.data is not None:
            application.cover_letter_submitted = form.cover_letter_submitted.data
        if form.follow_up_sent.data is not None:
            application.follow_up_sent = form.follow_up_sent.data
        if form.follow_up_message.data:
            application.follow_up_message = form.follow_up_message.data
        if form.notes.data:
            application.notes = form.notes.data
        
        new_interview_stages = []
        for stage_form in form.interview_stages.entries:
            if stage_form.data and stage_form.stage_name.data:
                # Check if this is an existing stage or a new one
                stage_id = stage_form.data.get("id")
                if stage_id:
                    # Update existing stage
                    stage = InterviewStage.query.get(stage_id)
                    if stage:
                        stage_form.populate_obj(stage)
                        new_interview_stages.append(stage)
                else:
                    # Add a new stage
                    new_stage = InterviewStage(job_application_id=application.id)
                    for field in ['stage_name', 'date', 'status', 'notes']:
                        if field in stage_form.data:
                            setattr(new_stage, field, stage_form.data[field])
                    new_interview_stages.append(new_stage)

        # Delete stages not in the updated list
        existing_stage_ids = {stage.id for stage in application.interview_stages}
        updated_stage_ids = {stage.id for stage in new_interview_stages if stage.id}

        for stage_id in existing_stage_ids - updated_stage_ids:
            stage_to_delete = InterviewStage.query.get(stage_id)
            db.session.delete(stage_to_delete)
        
        application.interview_stages = new_interview_stages 

        db.session.commit()
        flash('Job application updated successfully!', 'success')
        print(f"Updated application: {application}")
        return redirect(url_for('dashboard'))
    else:
        if form.errors:
            print("Form validation failed.")
            print("Errors:", form.errors)       
    
    return render_template('edit_application.html', form=form, application=application)

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

@app.route('/application/<int:application_id>/add_interview', methods=['GET', 'POST'])
@login_required
def add_interview_stage(application_id):
    form = InterviewStageForm()
    application = JobApplication.query.get_or_404(application_id)
    if form.validate_on_submit():
        new_stage = InterviewStage(
            job_application_id=application.id,
            stage_name=form.stage_name.data,
            date=form.date.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(new_stage)
        db.session.commit()
        flash('Interview stage added successfully.', 'success')
        return redirect(url_for('view_application', application_id=application.id))
    return render_template('add_interview_stage.html', form=form, application=application)

@app.route('/interview_stage/<int:stage_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_interview_stage(stage_id):
    stage = InterviewStage.query.get_or_404(stage_id)
    form = InterviewStageForm(obj=stage)
    if form.validate_on_submit():
        form.populate_obj(stage)
        db.session.commit()
        flash('Interview stage updated successfully.', 'success')
        return redirect(url_for('view_application', application_id=stage.job_application_id))
    return render_template('edit_interview_stage.html', form=form, stage=stage)

@app.route('/interview_stage/<int:stage_id>/delete', methods=['POST'])
@login_required
def delete_interview_stage(stage_id):
    stage = InterviewStage.query.get_or_404(stage_id)
    db.session.delete(stage)
    db.session.commit()
    flash('Interview stage deleted successfully.', 'success')
    return redirect(url_for('view_application', application_id=stage.job_application_id))

if __name__ == '__main__':
    app.run(debug=True)