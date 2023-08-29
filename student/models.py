# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:35:45 2022

@author: hp
"""
from flask_sqlalchemy import SQLAlchemy
from student import db,app,login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from student import bcrypt
import student.app as route
from flask import session


@login_manager.user_loader
def load_user(user_id):
    if session['type']=='user':
        return User.query.get(int(user_id))
    else:
        return Recruiter.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    phone_no = db.Column(db.String(length=10), nullable=False)
    lname = db.Column(db.String(length=50), nullable=False)
    fname = db.Column(db.String(length=50), nullable=False)
    mname = db.Column(db.String(length=50), nullable=False)
    sadditonal=db.relationship('Sadditional', backref='owned_user', lazy=True)
    
        
  
    @property
    def password(self):
        return self.password
  
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
        
'''
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
  
    def __repr__(self):
        return f'User {self.fname}'
    
    def __init__(self, username, password_hash, email_address, phone_no, lname, fname, mname):
        self.username = username
        self.password_hash = password_hash
        self.email_address = email_address
        self.phone_no = phone_no
        self.lname = lname
        self.fname = fname
        self.mname = mname
    
'''


class Recruiter(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    phone_no = db.Column(db.String(length=10), nullable=False)
    lname = db.Column(db.String(length=50), nullable=False)
    fname = db.Column(db.String(length=50), nullable=False)
    mname = db.Column(db.String(length=50), nullable=False)
    '''
    @login_manager.user_loader
    def load_user(user_id):
        return Recruiter.query.get(int(user_id))
    '''
    @property
    def password(self):
        return self.password
  
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
    
    
    
    
    def __repr__(self):
        return f'User {self.username}'
    
    
class Sadditional(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), db.ForeignKey('user.id'))
    dob = db.Column(db.String(length=20))
    gender = db.Column(db.String(length=10))
    state = db.Column(db.String(length=50))
    city = db.Column(db.String(length=30))
    address = db.Column(db.String(length=150))
    pin_code = db.Column(db.String(length=10))
    g_course = db.Column(db.String(length=100))   
    g_percentage = db.Column(db.String(length=10))
    g_institute = db.Column(db.String(length=100))
    g_yr = db.Column(db.String(length=10))   
    g_state = db.Column(db.String(length=50))
    g_city = db.Column(db.String(length=30))
    hd_class = db.Column(db.String(length=50))   
    hd_percentage = db.Column(db.String(length=10))
    hd_institute = db.Column(db.String(length=100))
    hd_pyr = db.Column(db.String(length=10))   
    hd_state = db.Column(db.String(length=50))
    hd_city = db.Column(db.String(length=30))
    ssc_class = db.Column(db.String(length=50))   
    ssc_percentage = db.Column(db.String(length=10))
    ssc_institute = db.Column(db.String(length=100))
    ssc_pyr = db.Column(db.String(length=10))   
    ssc_state = db.Column(db.String(length=50))
    ssc_city = db.Column(db.String(length=30))
    skill = db.Column(db.String(length=500))
    achievements = db.Column(db.String(length=1000))    
    previous_projects = db.Column(db.String(length=1000))
    git_url = db.Column(db.String(length=100))
    hobby = db.Column(db.String(length=200))
    work_exp = db.Column(db.String(length=1000))
    resume = db.Column(db.LargeBinary)
    txt_resume = db.Column(db.String(length=50))
    presume = db.Column(db.LargeBinary)
    txt_presume = db.Column(db.String(length=50))
    
    
class Radditional(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), db.ForeignKey('recruiter.id'))
    cname = db.Column(db.String(length=100))
    cstate = db.Column(db.String(length=50))
    ccity = db.Column(db.String(length=50))
    caddress = db.Column(db.String(length=500))
    cpin_code = db.Column(db.Integer())
    
class Jobs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), db.ForeignKey('recruiter.id'))
    cname = db.Column(db.String(length=100))
    ccity = db.Column(db.String(length=50))
    cstate = db.Column(db.String(length=50))
    caddress = db.Column(db.String(length=300))
    cqualification = db.Column(db.String(length=50))
    cposition = db.Column(db.String(length=100))
    csalary = db.Column(db.String(length=50))
    cdesc = db.Column(db.String(length=1000))

    
class Approved_students(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cname = db.Column(db.String(length=100), db.ForeignKey('jobs.cname'))
    cposition = db.Column(db.String(length=100), db.ForeignKey('jobs.cposition'))
    cstatus = db.Column(db.String(length=100))
    email_address = db.Column(db.String(length=50), nullable=False)
    phone_no = db.Column(db.String(length=10), nullable=False)
    lname = db.Column(db.String(length=50), nullable=False)
    fname = db.Column(db.String(length=50), nullable=False)
    mname = db.Column(db.String(length=50), nullable=False)
    dob = db.Column(db.String(length=20))
    gender = db.Column(db.String(length=10))
    state = db.Column(db.String(length=50))
    city = db.Column(db.String(length=30))
    address = db.Column(db.String(length=150))
    pin_code = db.Column(db.String(length=10))
    g_course = db.Column(db.String(length=100))   
    g_percentage = db.Column(db.String(length=10))
    g_institute = db.Column(db.String(length=100))
    skill = db.Column(db.String(length=500))
    txt_resume = db.Column(db.String(length=100))