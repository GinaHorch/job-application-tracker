from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from models import JobApplication, db
from forms import JobApplicationForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET','POST'])
def form():
    form = JobApplicationForm()
    if form.validate_on_submit():
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
        )
        return redirect(url_for('dashboard'))
    return render_template('form.html', form=form)

@app.route('/dashboard')
def dashboard():
    all_applications = JobApplication.query.all()

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

    return render_template('dashboard.html', applications=filtered_applications or all_applications)
    

if __name__ == '__main__':
    app.run(debug=True)