from flask_app import app 
from flask import render_template, redirect, request, session, url_for
from flask_app.models import user, product, category
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/products")
def get_products():
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("products.html", users=user.User.get_id(data), categories=category.Category.get_category_by_creator())

@app.route("/product/<int:id>")
def show_product(id):
    if "user_id" not in session: 
        return redirect('/logout')
    user_data = {
        "id" : session['user_id']
    }
    data = {
        "id": id
    }
    return render_template("allproducts.html", users=user.User.get_id(user_data), product=product.Product.get_one_product(data))

@app.route("/new-product", methods=['POST'])
def new_product():
    if not product.Product.validate_product(request.form):
        return redirect('/products')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "wholesale": request.form['wholesale'],
        "retail": request.form['retail'],
        "inventory": request.form['inventory'],
        "category_id": request.form['category_id'],
        "user_id": session['user_id']
    }
    product.Product.save_product(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_product(id):
    if "user_id" not in session:
        return redirect("/logout")
    user_data = {
        "id": session['user_id']
    }
    data = {
        "id": id
    }
    return render_template('edit.html', users=user.User.get_id(user_data), product=product.Product.get_one_product(data), categories=category.Category.get_category_by_creator())

@app.route("/update-product", methods=['POST'])
def update_product():
    if "user_id" not in session:
        return redirect("/logout")
    if not product.Product.validate_product(request.form):
        current_data = {
            "current_id" : request.form['id']
        }
        return redirect(url_for("update_product", id=current_data['current_id']))
    
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "wholesale": request.form['wholesale'],
        "retail": request.form['retail'],
        "inventory": request.form['inventory'],
        "category_id": request.form['category_id'],
        "user_id": session['user_id']
    }
    product.Product.edit_product(data)
    return redirect("/dashboard")

@app.route("/delete-product/<int:id>")
def delete_product(id):
    data = {
        "id": id
    }
    product.Product.delete_product(data)
    return redirect('/dashboard')

@app.route("/product-search")
def search():
    mysql = connectToMySQL("products")
    query = "SELECT * FROM products WHERE name LIKE %%(name)s AND user_id = %(user_id)s;"
    data = {
        "name": request.args.get('name') + "%",
        "user_id": session['user_id']
    }
    results = mysql.query_db(query, data)
    return render_template("show.html", this_product=results)