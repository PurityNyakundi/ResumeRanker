from fileinput import filename
from web import db
from web import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    details = db.relationship('Upload_db', backref='user', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Upload_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    detail = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_desc = db.Column(db.Integer, db.ForeignKey('job_db.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"


class Job_db(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(20), nullable=False)
    Jobtitle = db.Column(db.String(120), nullable=False)
    filename1 = db.Column(db.String(60), nullable=False)
    details = db.relationship('Upload_db', backref='job_db', lazy=True)
    def __repr__(self):
        return f"Job('{self.company}', '{self.Jobtitle}','{self.filename1}')"
