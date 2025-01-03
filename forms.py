from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Optional

csrf = CSRFProtect()

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

    cv_submitted = RadioField('CV Submitted', choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    cover_letter_submitted = RadioField('Cover Letter Submitted', choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    follow_up_sent = RadioField('Follow-up Message Sent', choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('n/a', 'N/A')
    ], validators=[DataRequired()])

    follow_up_message = TextAreaField('Follow-up Message (Optional)', validators=[Optional()])

    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Submit')