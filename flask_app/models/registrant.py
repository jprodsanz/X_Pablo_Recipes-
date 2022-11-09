from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Registrant: 
    
    db = "login_reg_x"

    def __init__(self,data): 

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO registrants (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM registrants;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM registrants WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM registrants WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(registrant):
        is_valid = True
        query = "SELECT * FROM registrants WHERE email = %(email)s;"
        results = connectToMySQL("login_reg_x").query_db(query,registrant)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        
        if not EMAIL_REGEX.match(registrant['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        
        if len(registrant['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        
        if len(registrant['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        
        if len(registrant['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        
        if registrant['password'] != registrant['confirm_password']:
            flash("Passwords don't match","register")
        
        return is_valid