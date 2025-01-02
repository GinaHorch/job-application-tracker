from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.Date, nullable=False)
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

    def __repr__(self):
        return f"<JobApplication {self.id} - {self.company}>"
