#Importing packages
import os

#Setting the configuration setting for the Flask App
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False