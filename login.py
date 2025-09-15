from flask import Flask, request, jsonify
import requests
import os
from flask_sqlalchemy import SQLAlchemy 
import psycopg2

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from bcrypt import hashpw, gensalt


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Root@localhost:5432/postgres' 
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
app.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager(app)

db=SQLAlchemy(app)

class User(db.Model):
     __tablename__='customer'
     id=db.Column(db.Integer,primary_key=True)
     username=db.Column(db.String(50),unique=True,nullable=False)
     email=db.Column(db.String(50),nullable=False)
     password=db.Column(db.String(500),nullable=False)
 
with app.app_context():
     db.create_all()


@app.route('/')
def login():
   
     return jsonify({"messages":"this page is for login"})

@app.route('/show')
def show():
     data = User.query.all()
     data_list = [
          {
               "username": user.username,
               "email": user.email,
          } for user in data
     ]
     return jsonify({"data": data_list})

@app.route('/register',methods=['POST'])
def add_user():
     username=request.json['username']
     email=request.json['email']
     password=request.json['password']
     if not username or not password:
        
        return jsonify({'error': 'Username and password required'}), 400
     
     hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
     ser=User(username=username,email=email,password=hashed_password)
     db.session.add(ser)
     db.session.commit()
     return jsonify({"message":"user added successfully"})

@app.route('/login',methods=['POST'])
def user_login():
     username=request.json['username']
     password=request.json['password']
     if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
     user=User.query.filter_by(username=username).first()
     if user:
          access_token = create_access_token(identity=username)
          headers = {'Authorization': f'Bearer {access_token}'}
          response = requests.get('http://localhost:5001/products', headers=headers)

          products = response.json().get('data', [])
          return jsonify({
            "access_token": access_token,
            "message": "Login successful",
            "products": products
        })

          
     
     else:
          return jsonify({"message":"invalid username or password"})


if __name__=='__main__':
     app.run(debug=True)

