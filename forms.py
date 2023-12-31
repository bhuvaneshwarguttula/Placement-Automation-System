# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:54:40 2022

@author: hp
"""

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, InputRequired
from student.models import User, Recruiter, Sadditional
from flask import session

class RegisterForm(FlaskForm):
    def validate_user(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a diffferent username')
    
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! please try a different email address')
        
    
    lname = StringField(label = "Last name",validators=[DataRequired()])
    fname = StringField(label = "First name",validators=[DataRequired()])
    mname = StringField(label = "Middle name",validators=[DataRequired()])
    phone_no = StringField(label = "Phone No.",validators=[DataRequired()])
    email_address = StringField(label = "Email", validators=[Email()])
    username = StringField(label="Username", validators=[Length(min=2,max=30),DataRequired()])
    password_hash = PasswordField(label="Create Password",validators=[Length(min=6),DataRequired()])
    password_hash1 = PasswordField(label="Confirm Password", validators=[EqualTo('password_hash1'),DataRequired()])
    submit = SubmitField(label = "Register Now")
    
    
        
    
class SLoginForm(FlaskForm):
    username=StringField(label="Username", validators=[DataRequired()])
    password_hash = PasswordField(label="Password",validators=[DataRequired()])
    login = SubmitField(label="Login")
    
class CLoginForm(FlaskForm):
    username=StringField(label="Username", validators=[DataRequired()])
    password_hash = PasswordField(label="Password",validators=[DataRequired()])
    login = SubmitField(label="Login")
    
class resumeform(FlaskForm):
    resume_pdf = FileField(label="resume",validators=[InputRequired()])
    submit = SubmitField(label="Save")
    
class resume_buildform(FlaskForm):
    submit = SubmitField(label="Save")
    
class CRegisterForm(FlaskForm):
    def validate_user(self,username_to_check):
        user = Recruiter.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Company already exists! Please try a diffferent username')
    lname = StringField(label = "Last name",validators=[DataRequired()])
    fname = StringField(label = "First name",validators=[DataRequired()])
    mname = StringField(label = "Middle name",validators=[DataRequired()])
    phone_no = StringField(label = "Phone No.",validators=[DataRequired()])
    email_address = StringField(label = "Email", validators=[Email()])
    username = StringField(label="Username", validators=[Length(min=2,max=30),DataRequired()])
    password_hash = PasswordField(label="Create Password",validators=[Length(min=6),DataRequired()])
    password_hash1 = PasswordField(label="Confirm Password", validators=[EqualTo('password_hash'),DataRequired()])
    submit = SubmitField(label = "Register Now")
    
    
class Sadditionalform(FlaskForm):
    def validate_user(self,username_to_check):
        user1 = Sadditional.query.filter_by(username=username_to_check.data).first()
        if user1:
             raise ValidationError('Company already exists! Please try a diffferent username')
    # #route.session.get('user', None)
    # #work=route.session['user']
    # route.user=session.get('user', None)
    # attempted_user1=Sadditional.query.filter_by(username=route.user).first()
    #username=StringField(label = "Username",validators=[DataRequired()])
    dob=StringField(label = "Date of birth",validators=[DataRequired()])     
    gender=SelectField(label = "Gender",description="Gender",choices=["Male","Female","Other"],validators=[DataRequired()])
    state=SelectField(label = "State",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    city=StringField(label = "City",validators=[DataRequired()])
    address=StringField(label = "Address",validators=[DataRequired()])
    pin_code=StringField(label = "Pin Code",validators=[DataRequired()])
    g_course=StringField(label = "Graduated in",validators=[DataRequired()])
    g_percentage=StringField(label = "Percentage/CGPA",validators=[DataRequired()])
    g_institute=StringField(label = "Name of your Institute",validators=[DataRequired()])
    g_yr=StringField(label = "Year of Graduation",validators=[DataRequired()])
    g_state=SelectField(label = "State",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    g_city=StringField(label = "City",validators=[DataRequired()])
    hd_class=SelectField(label = "Qualification Level",choices=["Qualification Level","H.S.C. (12th)","Diploma"],validators=[DataRequired()])
    hd_percentage=StringField(label = "Percentage/CGPA",validators=[DataRequired()])
    hd_institute=StringField(label = "Name of your Institute",validators=[DataRequired()])
    hd_pyr=StringField(label = "Passing Year",validators=[DataRequired()])
    hd_state=SelectField(label = "State",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    hd_city=StringField(label = "City",validators=[DataRequired()])
    ssc_class=StringField(label = "Qualification level",validators=[DataRequired()])
    ssc_percentage=StringField(label = "Percentage/CGPA",validators=[DataRequired()])
    ssc_institute=StringField(label = "Name of your Institute",validators=[DataRequired()])
    ssc_pyr=StringField(label = "Passing Year",validators=[DataRequired()])
    ssc_state=SelectField(label = "State",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    ssc_city=StringField(label = "City",validators=[DataRequired()])
    skill=TextAreaField(label = "Skills",validators=[DataRequired()])
    achievements=TextAreaField(label = "Achievements",validators=[DataRequired()])
    previous_projects=TextAreaField(label = "Previous Projects",validators=[DataRequired()])
    git_url=StringField(label = "GitHub URL",validators=[DataRequired()])
    hobby=TextAreaField(label = "Hobbies",default=None,validators=[DataRequired()])
    #work=attempted_user1.work_exp if attempted_user1 else ""
    work_exp=TextAreaField(label = "Description" ,validators=[DataRequired()])     
    submit = SubmitField(label = "Save Profile")
    

class Radditionalform(FlaskForm):
    def validate_user(self,username_to_check):
        user = Sadditional.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Company already exists! Please try a diffferent username')
            
    nameofc=StringField(label = "Name of the Company",validators=[DataRequired()])
    state=SelectField(label = "State",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    city=StringField(label = "City",validators=[DataRequired()])
    address=StringField(label = "Address",validators=[DataRequired()])
    pin_code=StringField(label = "Pin Code",validators=[DataRequired()])
    submit = SubmitField(label = "Save Profile")
    
class Jobform(FlaskForm):
    # cname = StringField(label = "Company:",validators=[DataRequired()])
    # ccity = StringField(label = "City:",validators=[DataRequired()])
    # cstate = SelectField(label = "cstate",choices=["Your State","Andhra Pradesh","Andaman and Nicobar Islands","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadar and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"],validators=[DataRequired()])
    # caddress = StringField(label = "Address:",validators=[DataRequired()])
    cqualification = StringField(label = "Qualification Required:",validators=[DataRequired()])
    cposition = StringField(label = "Position:",validators=[DataRequired()])
    csalary = StringField(label = "Salary Range:",validators=[DataRequired()])
    cdesc = TextAreaField(label = "Job Description:",validators=[DataRequired()])
    submit = SubmitField(label = "Save")
    
    
class applied_form(FlaskForm):
    #visibility: hidden;
    style={'style': 'width:10%; eight:5%; font-size: 0px; visibility: hidden;','readonly': True}
    apply = SubmitField(label = "Apply")
    value = StringField("Value",render_kw=style)
    value1 = StringField("cname",render_kw=style)
    
class send_approval(FlaskForm):
    style={'style': 'width:10%; eight:5%; font-size: 0px; visibility: hidden;','readonly': True}
    approve = SubmitField(label = "Approve")
    download = SubmitField(label = "Download Resume")
    txt_resume = StringField("resume",render_kw=style)
    position = StringField("resume",render_kw=style)
    
    
    
    
    
    
    
    
    
    