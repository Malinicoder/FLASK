import os
from datetime import timedelta

class Config:
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Root@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-this")  
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 
    JWT_ALGORITHM = "HS256"

    SECRET_KEY = os.getenv("SECRET_KEY", "flask-secret-key-change-this")
