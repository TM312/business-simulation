from datetime import datetime
from app import app, db, login, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt


class Subscriber(db.Model):
    __tablename__ = "subscriber"  # table name for SQAlchemy

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    signed_up = db.Column(db.DateTime, default=datetime.utcnow)

    # The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
    def __repr__(self):
        return 'id: {} | email: {} >'.format(self.id, self.email)

class User(UserMixin, db.Model):
    __tablename__ = "user" #table name for SQAlchemy

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  #, auto_now_add=True) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    title = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    simmodels = db.relationship('SimModel', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def avatar(self, size):  # The nice thing about making the User class responsible for returning avatar URLs is that if some day I decide Gravatar avatars are not what I want, I can just rewrite the avatar() method to return different URLs, and all the templates will start showing the new avatars automatically.
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
    def __repr__(self):
        return '<first_name: {} | email: {} | id: {}>'.format(self.first_name, self.email, self.id)


class SimModel(db.Model):
    __tablename__ = "sim_model"  # table name for SQAlchemy

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(64), index=True, unique=True)
    teaser = db.Column(db.String(140))
    introductory_text = db.Column(db.String(1000))
    infobox_context = db.Column(db.String(1000))

    # control_inputs = db.relationship(
    #     'ControlInput', backref='model', lazy=True)
    # environment_inputs = db.relationship(
    #     'EnvironmentInput', backref='model', lazy=True)
    # kpis = db.relationship('KPI', backref='model', lazy=True)

    time_horizon = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#UserSchema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

#SimModelSchema 
class SimModelSchema(ma.ModelSchema):
    class Meta:
        model = SimModel




