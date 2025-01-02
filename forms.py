from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class JobApplicationForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    title = StringField('Job Title', validators=[DataRequired()])
    status = SelectField('Application Status', choices=[
        ('Applied', 'Applied'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Offer Received', 'Offer Received'),
        ('Rejected', 'Rejected'),
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')
