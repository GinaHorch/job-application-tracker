from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Optional, EqualTo, ValidationError
from models import User

csrf = CSRFProtect()

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class JobApplicationForm(FlaskForm):
    date_submitted = DateField('Date Application Submitted', format='%d-%m-%Y', validators=[Optional()])
    due_date = DateField('Application Closing Date', format='%d-%m-%Y', validators=[Optional()])
    follow_up_date = DateField('Follow-up Reminder Date', format='%d-%m-%Y', validators=[Optional()])
    company = StringField('Company Name', validators=[DataRequired()])
    contact = StringField('Recruiter/Company Contact', validators=[DataRequired()])
    position_title = StringField('Job Title Applied for', validators=[DataRequired()])
    status = SelectField('Application Status', choices=[
        ('Work in progress', 'Work in progress'),
        ('Applied', 'Applied'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Offer Received', 'Offer Received'),
        ('Rejected', 'Rejected'),
    ], validators=[DataRequired()])

    cv_submitted = SelectField('CV Submitted', choices=[
        ('yes', 'Yes'), 
        ('no', 'No'), 
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    cover_letter_submitted = SelectField('Cover Letter Submitted', choices=[
        ('yes', 'Yes'), 
        ('no', 'No'), 
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    follow_up_sent = SelectField('Follow-up Message Sent', choices=[
        ('yes', 'Yes'), 
        ('no', 'No'), 
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    follow_up_message = TextAreaField('Follow-up Message (Optional)', validators=[Optional()])

    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Submit')