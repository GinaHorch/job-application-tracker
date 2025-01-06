from flask_login import UserMixin
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    company = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=True)
    position_title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    cv_submitted = db.Column(db.String(10), nullable=False)
    cover_letter_submitted = db.Column(db.String(10), nullable=False)
    follow_up_sent = db.Column(db.String(10), nullable=False)
    follow_up_message = db.Column(db.Text, nullable=True)
    # interview_stages = db.relationship('InterviewStage', back_populates='job_application', cascade='all, delete-orphan')
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('job_applications', lazy=True))

    @hybrid_property
    def priority(self):
        today = datetime.utcnow().date()
        if self.due_date and self.due_date <= today + timedelta(days=2):
            return 'high'
        elif self.status == 'Offer Received':
            return 'completed'
        else:
            return 'normal'
        
    @priority.expression
    def priority(cls):
        return case(
            (cls.due_date <= datetime.utcnow().date() + timedelta(days=2), 'high'),
            (cls.status == 'Offer Received', 'completed'),
            else_='normal'
        )   

    def __repr__(self):
        return f"<JobApplication {self.id} - {self.company}>"

class InterviewStage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_application_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=False)
    stage_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    job_application = db.relationship('JobApplication', 
                                      backref=db.backref('interview_stages', lazy=True, cascade='all, delete-orphan'))