from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user, category

class Product:
    db = "products"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.wholesale = data['wholesale']
        self.retail = data['retail']
        self.inventory = data['inventory']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None
        self.category_id = None
    
    @classmethod
    def save_product(cls, data):
        query = "INSERT INTO products (name, description, wholesale, retail, inventory, created_at, updated_at, user_id, category_id) VALUES (%(name)s, %(description)s, %(wholesale)s, %(retail)s, %(inventory)s, NOW(), NOW(), %(user_id)s, %(category_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_product(cls, data):
        query = "UPDATE products SET name=%(name)s, description=%(description)s, wholesale=%(wholesale)s, retail=%(retail)s, inventory=%(inventory)s, user_id=%(user_id)s, category_id=%(category_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_product(cls,data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_products_by_creator(cls):
        query = "SELECT * FROM products LEFT JOIN users ON products.user_id = users.id LEFT JOIN categories ON products.category_id = categories.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_products = []
        for row in results:
            one_product = cls(row)
            user_info = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            category_info = {
                "id" : row['categories.id'],
                "name": row['categories.name'],
                "created_at": row['categories.created_at'],
                "updated_at": row['categories.updated_at'],
                "user_id": row['categories.user_id']
            }
            creator = user.User(user_info)
            many = category.Category(category_info)
            one_product.user_id = creator
            one_product.category_id = many
            all_products.append(one_product)

        return all_products


    @staticmethod
    def validate_product(product):
        is_valid = True
        if len(product['name']) < 3:
            flash('product name must be at least 3 characters!', 'product')
            is_valid = False
        if len(product['description']) < 3:
            flash('product description must be at least 3 characters!', 'product')
            is_valid = False
        if product['wholesale']  == '':
            flash('wholesale price is required!', 'product')
            is_valid = False
        if product['retail']  == '':
            flash('retail price is required!', 'product')
            is_valid = False
        if product['inventory']  == '':
            flash('inventory is required!', 'product')
            is_valid = False
        return is_valid