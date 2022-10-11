from flask_app import app 
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, product, category
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def start():
    return redirect("/login")

@app.route("/login")
def index():
    return render_template("index.html")

@app.route("/register")
def index2():
    return render_template("index2.html")

@app.route("/register-user", methods=['POST'])
def register():
    if not user.User.validate_register(request.form):
        return redirect("/register")
    data = {
        "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = user.User.save_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route("/login-user", methods=['POST'])
def login():
    users = user.User.get_email(request.form)
    if not users:
        flash("Invalid Email/Password", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect("/login")
    session['user_id'] = users.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }

    return render_template("dashboard.html", users=user.User.get_id(data), categories=category.Category.get_category_by_creator(), products=product.Product.get_products_by_creator())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")