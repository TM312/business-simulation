from flask import render_template, flash, redirect, jsonify, request, url_for #operation that converts a template into a complete HTML page is called rendering
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse # To determine if the URL is relative or absolute, I parse it with Werkzeug's url_parse() function
                                    # and then check if the netloc component is set or not (s.u.).

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, SignupForm
from app.models import User, SimModel#, ControlInput, EnvironmentInput, KPI
from app.models import UserSchema, SimModelSchema#, ControlInputSchema, EnvironmentInputSchema, KPISchema
from app.email import send_password_reset_email

from random import sample #only for test purposes of chartist.js

import json
import datetime


@app.context_processor
def inject_footer_details():
    return dict(year=datetime.datetime.now().year, company_name=app.config['COMPANY_NAME'])

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    teaser = "The mechanisms behind a shared scooter operator’s business."

    form = SignupForm()
    if form.validate_on_submit():
        subscriber = Subscriber(email=form.email.data)
        db.session.add(subscriber)
        db.session.commit()
        flash('Everything worked out! You successfully subscribed to updates related to my research.')

    return render_template('index.html', teaser=teaser, title='Index', form=form)

@app.route('/example', methods=['GET', 'POST'])
def example():
    with open('./app/exampleModel.json') as exampleModel:
        model = json.load(exampleModel)

    return render_template('example.html', title='Example', model=model)

#test route
@app.route('/test')
def test():

    model = {
        "timeframe":7,
        "environment_inputs": [
        {"id": 1,
         "name": "Berlin Population",
         "description": "As of Q4 2018 the population of Berlin lies at ~3’644’000 and is expected to grow by 30’000 per year for the near future. Given that the characteristics Berlin’s population remains relatively stable within the time horizon, it is a good input for subsequent estimations of potential users.",
         "input_type": "static",
         "value_min": 0.05,
         "value_max": 0.3,
         "value_default": 0.05,
         "step": 0.05,
         }],

        # {"id": 2,
        #  "name": "Berlin Rider Share",
        #  "input_type": "linear",
        #  "value_min": 1,
        #  "value_max": 2,
        #  "value_default": 2,
        #  "step": 1,
        #  }]
    }

    return render_template('test.html', title='Test', model=model)

#API: get all users
@app.route('/api/users')
def users():
    users_schema = UserSchema(many=True)
    all_users = User.query.all()
    users = users_schema.dump(all_users)
    return jsonify({'users': users})

#API: get one user
@app.route('/api/users/<id>')
def get_user(id):
    user_schema = UserSchema()
    user = User.query.get(id)
    return user_schema.jsonify(user)

#API: get all models of a user
@app.route('/api/<id>/models')
def models(id):
    models_schema = SimModelSchema(many=True)
    all_models = SimModel.query.all()
    models = models_schema.dump(all_models)
    return jsonify({'models': models})

#API: get one model of one user
@app.route('/api/<id>/<model_id>')
def get_model(id, model_id):
    model_schema = SimModelSchema()
    model = SimModel.query.get(id)
    return model_schema.jsonify(model)









#route for API maybe transferred to '/api/data' or similar
@app.route('/jsonmodel')
def jsonmodel():
    with open('./app/exampleModel.json') as exampleModel:
        model = json.load(exampleModel)
    return jsonify(model)









#test route
@app.route('/jstest')
def jstest():
    return render_template('jstest.html', title='JSTest')

#test route
@app.route('/data')
def data():
    # with open('./app/exampleModel.json') as exampleModel:
    #     model = json.load(exampleModel)
    return jsonify({'results' : sample(range(1,10), 5)})

#unfinished
@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy')


# #Create a Model
# @app.route('/profile/<id>', methods=['POST'])
# def add_product(id):
#         # Init schema
#     simmodel_schema = SimModelSchema()

#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']

#     new_product = Product(name, description, price, qty)

#     db.session.add(new_product)
#     db.session.commit()

#     return product_schema.jsonify(new_product)

# #Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#     product = Product.query.get(id)

#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']

#     product.name = name
#     product.description = description
#     product.price = price
#     product.qty = qty

#     db.session.commit()

#     return product_schema.jsonify(product)

# #Get all Users
# @app.route('/product', methods=['GET'])
# def get_products():
#     simmodels_schema = SimModelSchema(many=True)

#     all_products = Product.query.all()
#     result = simmodels_schema.dump(all_products)
#     return jsonify(result)

# #Get single Product
# @app.route('/product/<id>', methods=['GET'])
# def get_product(id):
#     product = Product.query.get(id)
#     return product_schema.jsonify(product)

# #Delete single Product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#     product = Product.query.get(id)
#     db.session.delete(product)
#     db.session.commit()
#     return product_schema.jsonify(product)


@app.route('/login', methods=['GET', 'POST']) #this view function accepts GET and POST requests
def login():
    if current_user.is_authenticated: # The current_user variable comes from Flask-Login and can be used at any time during the handling
                                      # to obtain the user object that represents the client of the request.
                                      # The value of this variable can be a user object from the database
                                      # (which Flask-Login reads through the user_loader callback in models.py),
                                      # or a special anonymous user object if the user did not log in yet.

                                      # is_authenticated checks if the user is logged in or not
        return redirect(url_for('index')) #endpoint – the endpoint of the URL (name of the function)
    form = LoginForm()
    if form.validate_on_submit(): # The form.validate_on_submit() method does all the form processing work, i.e. gather all the data, run all the validators attached to fields, and if everything is all right it will return True
        user = User.query.filter_by(email=form.email.data).first() #first(): returns the user object if it exists, or None if it does not.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for('login')) # instructs the client web browser to automatically navigate to a different page, given as an argument
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # Flask provides a request variable that contains all the information that the client sent with the request.
                                             # In particular, the request.args attribute exposes the contents of the query string in a dict format.
        if not next_page or url_parse(next_page).netloc != '': #ensures that "next page" stays within the application
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(title=form.title.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile/<id>')
@login_required
def profile(id):
    profile = User.query.filter_by(id=id).first_or_404()

    models = [  #mockup var
        {'owner': profile, 'body': 'Example model #1'},
        {'owner': profile, 'body': 'Example model #2'}
    ]
    return render_template('profile.html', profile=profile, models=models)


@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('editProfile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('editProfile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
