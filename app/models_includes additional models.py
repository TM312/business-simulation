# from datetime import datetime
# from app import app, db, login, ma
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from hashlib import md5
# from time import time
# import jwt

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

    def __init__(self, date_created, title, first_name, last_name, email, password_hash, last_seen, simmodels):
        self.date_created
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.last_seen = last_seen
        self.simmodels = simmodels

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

    def avatar(self, size): # The nice thing about making the User class responsible for returning avatar URLs is that if some day I decide Gravatar avatars are not what I want, I can just rewrite the avatar() method to return different URLs, and all the templates will start showing the new avatars automatically.
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self): #The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
        return '<first_name: {} | email: {} | id: {}>'.format(self.first_name, self.email, self.id)


#UserSchema Schema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class SimModel(db.Model):
    __tablename__ = "sim_model" #table name for SQAlchemy

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(64), index=True, unique=True)
    teaser = db.Column(db.String(140))
    introductory_text = db.Column(db.String(1000))
    infobox_context = db.Column(db.String(1000))

    control_inputs = db.relationship('ControlInput', backref='model', lazy=True)
    environment_inputs = db.relationship('EnvironmentInput', backref='model', lazy=True)
    kpis = db.relationship('KPI', backref='model', lazy=True)

    time_horizon = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, model_name, teaser, introductory_text, infobox_context, control_inputs, environment_inputs, kpis, time_horizon, owner_id):
        self.model_name = model_name
        self.teaser = teaser
        self.introductory_text = introductory_text
        self.infobox_context = infobox_context
        self.control_inputs = control_inputs
        self.environment_inputs = environment_inputs
        self.kpis = kpis
        self.time_horizon = time_horizon
        self.owner_id = owner_id
    
    def __repr__(self): #The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
        return '<model name {}>'.format(self.modelname)

#Simmodel Schema
class SimModelSchema(ma.ModelSchema):
    class Meta:
        fields = SimModel

class ControlInput(db.Model):
    __tablename__ = 'control_input'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000))
    sources = db.Column(db.String(500))
    model_id = db.Column(db.Integer, db.ForeignKey('sim_model.id'), nullable=False)

    value_min = db.Column(db.Integer)
    value_max = db.Column(db.Integer)
    value_default = db.Column(db.Integer)
    step = db.Column(db.Integer)
    input_type = db.Column(db.Integer, nullable=False) #0:static, 1:linear, 2:dynamic

    growth_factor = db.Column(db.Integer) #allows to differentiate between static and dynamic/growth inputs


    def __init__(self, name, description, sources, model_id):
        self.name = last_name
        self.description = description
        self.sources = sources
        self.value_min = value_min
        self.value_max = value_max
        self.steps = steps
        self.input_type = input_type
        self.growth_factor = growth_factor


    def __repr__(self): #The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
        return '<name {}>'.format(self.name)

    # __mapper_args__ = {
    #     'polymorphic_identity':'control_input',
    #     'polymorphic_on':type
    # }

#ControlInput Schema
# class ControlInputSchema(ma.ModelSchema):
#     class Meta:
#         fields = ControlInput

class EnvironmentInput(db.Model):
    __tablename__ = "environment_input"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000))
    sources = db.Column(db.String(500))

    value_min = db.Column(db.Integer)
    value_max = db.Column(db.Integer)
    value_default = db.Column(db.Integer)
    step = db.Column(db.Integer)
    input_type = db.Column(db.String)  # static, linear, exponential

    growth_factor = db.Column(db.Integer) #allows to differentiate between static and dynamic/growth inputs

    model_id = db.Column(db.Integer, db.ForeignKey('sim_model.id'))

    

    def __repr__(self): #The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
        return '<name {}>'.format(self.name)

#EnvironmentInput Schema
# class EnvironmentInputSchema(ma.ModelSchema):
#     class Meta:
#         fields = EnvironmentInput

class KPI(db.Model):
    __tablename__ = "kpi" #table name for SQAlchemy

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000))

    model_id = db.Column(db.Integer, db.ForeignKey('sim_model.id'), nullable=False)

    visible = db.Column(db.Boolean)

    def changeVisibility(self, visible):
        self.visible = visible

    def __repr__(self): #The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
        return '<name {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#KPI Schema
class KPISchema(ma.ModelSchema):
    class Meta:
        fields = KPI
