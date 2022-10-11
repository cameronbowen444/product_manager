from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user, product

class Category:
    db = "products"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None
        self.products = []
    
    @classmethod
    def save_category(cls, data):
        query = "INSERT INTO categories (name, created_at, updated_at, user_id) VALUES (%(name)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_category(cls, data):
        query = "UPDATE FROM categories SET name=%(name)s, user_id=%(user_id)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_category(cls, data):
        query = "DELETE FROM categories WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_one_category(cls,data):
        query = "SELECT * FROM categories WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_products_by_category(cls, data):
        query = "SELECT * FROM categories LEFT JOIN products ON categories.id = products.category_id WHERE categories.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        category = cls(results[0])
        for row in results:
            product_info = {
                "id": row["products.id"],
                "name": row["products.name"],
                "description": row["description"],
                "wholesale": row["wholesale"],
                "retail": row["retail"],
                "inventory": row["inventory"],
                "created_at": row["products.created_at"],
                "updated_at": row["products.updated_at"],
                "user_id": row["user_id"],
                "category_id": row["category_id"]
            }
            category.products.append(product.Product(product_info))
        return category

    @classmethod
    def get_category_by_creator(cls):
        query = "SELECT * FROM categories JOIN users ON categories.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) == 0:
            return []
        else:
            all_categories = []
            for row in results:
                one_category = cls(row)
                user_info = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                author = user.User(user_info)
                one_category.user_id = author
                all_categories.append(one_category)
            return all_categories

    @staticmethod
    def validate_category(category):
        is_valid = True
        if len(category['name']) < 3:
            flash('Category name must be at least 3 characters!', 'category')
            is_valid = False
        return is_valid