from flask_app import app 
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import user, product, category
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/new-category", methods=['POST'])
def new_category():
    if not category.Category.validate_category(request.form):
        return redirect('/dashboard')
    data = {
        "name": request.form['name'],
        "user_id": session['user_id']
    }
    category.Category.save_category(data)
    return redirect("/dashboard")

@app.route("/dashboard/<int:id>")
def category_id(id):
    user_data = {
        "id": session['user_id']
    }
    data = {
        "id": id
    }
    return render_template("dash.html", users=user.User.get_id(user_data), categories=category.Category.get_category_by_creator(), products=category.Category.get_products_by_category(data))

@app.route("/delete-category/<int:id>")
def delete_category(id):
    data = {
        "id": id
    }
    category.Category.delete_category(data)
    return redirect('/dashboard')