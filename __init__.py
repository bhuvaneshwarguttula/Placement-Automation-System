# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:51:44 2022

@author: hp
"""


from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db' #random name of file with extension .db
app.config['SECRET_KEY'] = 'ec9439cfc6c795ae2029594d'
db = SQLAlchemy(app)
#login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#URI - uniform resource identifier
#to create database from market import db and then type db.create_all

#from student import routes