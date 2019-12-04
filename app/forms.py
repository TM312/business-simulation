from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Subscriber
#from app.models import SimModel, ControlInput


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Enter your email here"})
    submit = SubmitField('Submit')

    def validate_email(self, email):
            subscriber = Subscriber.query.filter_by(email=email.data).first()
            if subscriber is not None:
                raise ValidationError('You are already signed up.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Title"})
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "First name"})
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email adress"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Repeat password"}) # EqualTo, which will make sure that its value is equal to the one for the first password field
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('A user with this email has already been registered.')

class EditProfileForm(FlaskForm):
    title = StringField('Title')
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)]) #max 140 --> 140 characters
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            emailexistscheck = User.query.filter_by(email=self.email.data).first()
            if emailexistscheck is not None:
                raise ValidationError('A user with this email has already been registered. Please use a different one.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class SimModelCreationForm(FlaskForm):
    model_name = StringField('Model name', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_modelname(self, modelname):
        modelnameexistscheck = User.query.filter_by(modelname=modelname.data).first()
        if modelnameexistscheck is not None:
            raise ValidationError('This name has already been assigned to one of your models. Please choose a different one.')

class EditSimModelForm(FlaskForm):
    model_name = StringField('Model name', validators=[DataRequired()])
    teaser = TextAreaField('Teaser text', validators=[Length(min=0, max=140)])
    introductory_text = TextAreaField('Introductory text', validators=[Length(min=0, max=1000)])
    infobox_context = TextAreaField('Infobox about Context', validators=[Length(min=0, max=1000)])

    submit = SubmitField('Submit')

    def __init__(self, original_model_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_model_name = original_model_name

    def validate_modelname(self, modelname):
        modelnameexistscheck = User.query.filter_by(modelname=modelname.data).first()
        if modelnameexistscheck is not None:
            raise ValidationError('This name has already been assigned to one of your models. Please choose a different one.')

class CreateSimModelNarrative(FlaskForm):
    teaser = TextAreaField('Teaser text', validators=[Length(min=0, max=140)])
    introductory_text = TextAreaField('Introductory text', validators=[Length(min=0, max=1000)])
    infobox_context = TextAreaField('Infobox about the context', validators=[Length(min=0, max=1000)])
