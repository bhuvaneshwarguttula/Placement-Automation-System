from flask import Flask, redirect, render_template, url_for, request, flash, get_flashed_messages, send_file, send_from_directory, make_response
from student import db,login_manager,app
from student.forms import RegisterForm, CRegisterForm, SLoginForm, CLoginForm, Sadditionalform, Radditionalform, resumeform, resume_buildform, Jobform, applied_form, send_approval
from io import BytesIO
#from flask_bcrypt import Bcrypt
from student.models import User, Recruiter, Sadditional, Radditional, Jobs, Approved_students
from flask_login import login_user,logout_user
from flask import session
from werkzeug.utils import secure_filename     
import os
import pdfkit
import time

#app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db' #random name of file with extension .db
app.config['SECRET_KEY'] = 'ec9439cfc6c795ae2029594d'
#db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#login_manager.init_app(app)

@app.route("/")
@app.route("/home")
def home():
    user_type=session.get('type', None)
    return render_template("index.html",user_type=user_type)


@app.route("/companies")
def companies():
    return render_template("companies.html")


@app.route("/aboutus")
def aboutus():
    return render_template("about us.html")


@app.route("/resumebuilder")
def resumebuilder():
    user=session.get('user', None)
    
    attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    attempted_user1 = Sadditional.query.filter_by(username=user).first() #used first to grab the data
    if attempted_user and attempted_user1:
        lname=attempted_user.lname
        fname=attempted_user.fname
        mname=attempted_user.mname
        phone_no=attempted_user.phone_no
        email_address=attempted_user.email_address
        dob=attempted_user1.dob
        gender=attempted_user1.gender
        state=attempted_user1.state
        city=attempted_user1.city
        address=attempted_user1.address
        pin_code=attempted_user1.pin_code
        g_course=attempted_user1.g_course
        g_percentage=attempted_user1.g_percentage
        g_institute=attempted_user1.g_institute
        g_yr=attempted_user1.g_yr
        g_state=attempted_user1.g_state
        g_city=attempted_user1.g_city
        hd_class=attempted_user1.hd_class
        hd_percentage=attempted_user1.hd_percentage
        hd_institute=attempted_user1.hd_institute
        hd_pyr=attempted_user1.hd_pyr
        hd_state=attempted_user1.hd_state
        hd_city=attempted_user1.hd_city
        ssc_class=attempted_user1.ssc_class
        ssc_percentage=attempted_user1.ssc_percentage
        ssc_institute=attempted_user1.ssc_institute
        ssc_pyr=attempted_user1.ssc_pyr
        ssc_state=attempted_user1.ssc_state
        ssc_city=attempted_user1.ssc_city
        skill=attempted_user1.skill
        achievements=attempted_user1.achievements
        previous_projects=attempted_user1.previous_projects
        git_url=attempted_user1.git_url
        hobby=attempted_user1.hobby
        work_exp=attempted_user1.work_exp
    
    return render_template("resumebuilder.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp)


@app.route("/sampleresume")
def sampleresume():
    return render_template("sampleresume.html")


@app.route("/sign-in student",methods=['GET','POST'])
def signinstudent():
    
    form = SLoginForm()
    
    if form.validate_on_submit() and request.method=='POST':
        attempted_user = User.query.filter_by(username=form.username.data).first() #used first to grab the data    
        if attempted_user:
            if attempted_user.check_password_correction(attempted_password=form.password_hash.data):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                session['user']=form.username.data
                session['type']="user"
                return redirect(url_for('studentprofile'))
            else:
                flash('Username and password are not matched! Plese try again',category='danger')
    
    return render_template("signin student.html",form=form)


@app.route("/sign-in recruiter",methods=['GET','POST'])
def signinrecruiter():
    form = CLoginForm()
    if form.validate_on_submit() and request.method=='POST':
        attempted_ruser = Recruiter.query.filter_by(username=form.username.data).first() #used first to grab the data
        if attempted_ruser:
            if attempted_ruser.check_password_correction(attempted_password=form.password_hash.data):
                login_user(attempted_ruser)
                session['user']=form.username.data
                session['type']="recruiter"
                flash(f'Success! You are logged in as: {attempted_ruser.username}', category='success')
                return redirect(url_for('recruiterprofile'))
        else:
            flash('Username and password are not matched! Plese try again',category='danger')
    
    return render_template("signin recruiter.html",form=form)


@app.route("/sign-up student",methods=['GET','POST'])
def signupstudent():
    form = RegisterForm()
    #if form.validate_on_submit():
    if form.validate_on_submit() and request.method=='POST':
        user = User(
                username = form.username.data,
                password = form.password_hash.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                lname = form.lname.data,
                fname = form.fname.data,
                mname = form.mname.data
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'there was error: {err_msg}')
        
    
    return render_template("signup student.html",form=form)


@app.route("/sign-up recruiter",methods=['GET','POST'])
def signuprecruiter():
    form = CRegisterForm()
    
    if form.validate_on_submit() and request.method=='POST':
        user = Recruiter(
                username= form.username.data,
                password = form.password_hash.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                lname = form.lname.data,
                fname = form.fname.data,
                mname = form.mname.data
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash('there was error: {err_msg}')
    return render_template("signup recruiter.html",form=form)


@app.route("/student profile", methods=['GET','POST'])
def studentprofile():
    form = resume_buildform()
    user=session.get('user', None)
    
    attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    if attempted_user:
        lname=attempted_user.lname
        fname=attempted_user.fname
        mname=attempted_user.mname
        phone_no=attempted_user.phone_no
        email_address=attempted_user.email_address
    
    attempted_user1 = Sadditional.query.filter_by(username=user).first()
    #if attempted_user1:
    if attempted_user1:
            # state=attempted_user1.state
            # g_state=attempted_user1.g_state
            # form.hd_class.data=attempted_user1.hd_class
            # form.hd_state.data=attempted_user1.hd_state
            # form.ssc_state.data=attempted_user1.ssc_state
            # form.skill.data=attempted_user1.skill
            # form.previous_projects.data=attempted_user1.previous_projects
            # form.achievements.data=attempted_user1.achievements
            # form.hobby.data=attempted_user1.hobby
            # form.work_exp.data=attempted_user1.work_exp
            
            
            dob=attempted_user1.dob
            gender=attempted_user1.gender
            state=attempted_user1.state
            city=attempted_user1.city
            address=attempted_user1.address
            pin_code=attempted_user1.pin_code
            g_course=attempted_user1.g_course
            g_percentage=attempted_user1.g_percentage
            g_institute=attempted_user1.g_institute
            g_yr=attempted_user1.g_yr
            g_state=attempted_user1.g_state
            g_city=attempted_user1.g_city
            hd_class=attempted_user1.hd_class
            hd_percentage=attempted_user1.hd_percentage
            hd_institute=attempted_user1.hd_institute
            hd_pyr=attempted_user1.hd_pyr
            hd_state=attempted_user1.hd_state
            hd_city=attempted_user1.hd_city
            ssc_class=attempted_user1.ssc_class
            ssc_percentage=attempted_user1.ssc_percentage
            ssc_institute=attempted_user1.ssc_institute
            ssc_pyr=attempted_user1.ssc_pyr
            ssc_state=attempted_user1.ssc_state
            ssc_city=attempted_user1.ssc_city
            skill=attempted_user1.skill
            achievements=attempted_user1.achievements
            previous_projects=attempted_user1.previous_projects
            git_url=attempted_user1.git_url
            hobby=attempted_user1.hobby
            work_exp=attempted_user1.work_exp
            
    if form.validate_on_submit() and request.method=='POST':
    #     #path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #     #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    #     rendered = render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,form=form)
    #     css=['templates/base2.html']
    #     pdf = pdfkit.from_string(rendered, False,css=css, options={"enable-local-file-access": ""})
    #     response = make_response(pdf)
    #     response.headers['Content-Type'] = 'application/pdf'
    #     response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    #     return response    
        render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,form=form)
    if attempted_user1:
        # rendered = render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address, form=form)
        # pdf = pdfkit.from_string(rendered, False)
        # response = make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'inline;filename=output.pdf'
        
        return render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,form=form)
    else:
        return render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address, form=form)
    #return render_template("student profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,form=form)

@app.route("/recruiter profile")
def recruiterprofile():
    recruiter=session.get('user', None)
    attempted_user = Recruiter.query.filter_by(username=recruiter).first() #used first to grab the data
    if attempted_user:
        lname=attempted_user.lname
        fname=attempted_user.fname
        mname=attempted_user.mname
        phone_no=attempted_user.phone_no
        email_address=attempted_user.email_address
    
    attempted_recruit = Radditional.query.filter_by(username=recruiter).first() #used first to grab the data
    if attempted_recruit:
        cname = attempted_recruit.cname
        cstate = attempted_recruit.cstate
        ccity = attempted_recruit.ccity
        caddress = attempted_recruit.caddress
        cpin_code = attempted_recruit.cpin_code
        
    if attempted_recruit:
        return render_template("recruiter profile.html",lname=lname,fname=fname,mname=mname,phone_no=phone_no,email_address=email_address,cname=cname,cstate=cstate,ccity=ccity,caddress=caddress,cpin_code=cpin_code)
    else:
        return render_template("recruiter profile.html",lname=lname,fname=fname,mname=mname,phone_no=phone_no,email_address=email_address)

@app.route("/student editprofile",methods=['POST','GET'])
def studenteditprofile():
    user=session.get('user', None)
    form=Sadditionalform()
    
    attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    if attempted_user:
        lname=attempted_user.lname
        fname=attempted_user.fname
        mname=attempted_user.mname
        phone_no=attempted_user.phone_no
        email_address=attempted_user.email_address
        
        
    attempted_user1=Sadditional.query.filter_by(username=user).first()
    if attempted_user1:
        
                
        
        dob=attempted_user1.dob
        gender=attempted_user1.gender
        state=attempted_user1.state
        city=attempted_user1.city
        address=attempted_user1.address
        pin_code=attempted_user1.pin_code
        g_course=attempted_user1.g_course
        g_percentage=attempted_user1.g_percentage
        g_institute=attempted_user1.g_institute
        g_yr=attempted_user1.g_yr
        g_state=attempted_user1.g_state
        g_city=attempted_user1.g_city
        hd_class=attempted_user1.hd_class
        hd_percentage=attempted_user1.hd_percentage
        hd_institute=attempted_user1.hd_institute
        hd_pyr=attempted_user1.hd_pyr
        hd_state=attempted_user1.hd_state
        hd_city=attempted_user1.hd_city
        ssc_class=attempted_user1.ssc_class
        ssc_percentage=attempted_user1.ssc_percentage
        ssc_institute=attempted_user1.ssc_institute
        ssc_pyr=attempted_user1.ssc_pyr
        ssc_state=attempted_user1.ssc_state
        ssc_city=attempted_user1.ssc_city
        skill=attempted_user1.skill
        achievements=attempted_user1.achievements
        previous_projects=attempted_user1.previous_projects
        git_url=attempted_user1.git_url
        hobby=attempted_user1.hobby
        work_exp=attempted_user1.work_exp
        
        # form.state.data=attempted_user1.state
        # form.g_state.data=attempted_user1.g_state
        # form.hd_class.data=attempted_user1.hd_class
        # form.hd_state.data=attempted_user1.hd_state
        # form.ssc_state.data=attempted_user1.ssc_state
        # form.skill.data=attempted_user1.skill
        # form.previous_projects.data=attempted_user1.previous_projects
        # form.achievements.data=attempted_user1.achievements
        # form.hobby.data=attempted_user1.hobby
        # form.work_exp.data=attempted_user1.work_exp
    
    if form.validate_on_submit() and request.method=='POST':
        
        attempted_user1=Sadditional.query.filter_by(username=user).first()
        if attempted_user1:
            attempted_user1.dob=form.dob.data
            attempted_user1.gender=form.gender.data
            attempted_user1.state=form.state.data
            attempted_user1.city=form.city.data
            attempted_user1.address=form.address.data
            attempted_user1.pin_code=form.pin_code.data
            attempted_user1.g_course=form.g_course.data
            attempted_user1.g_percentage=form.g_percentage.data
            attempted_user1.g_institute=form.g_institute.data
            attempted_user1.g_yr=form.g_yr.data
            attempted_user1.g_state=form.g_state.data
            attempted_user1.g_city=form.g_city.data
            attempted_user1.hd_class=form.hd_class.data
            attempted_user1.hd_percentage=form.hd_percentage.data
            attempted_user1.hd_institute=form.hd_institute.data
            attempted_user1.hd_pyr=form.hd_pyr.data
            attempted_user1.hd_state=form.hd_state.data
            attempted_user1.hd_city=form.hd_city.data
            attempted_user1.ssc_class=form.ssc_class.data
            attempted_user1.ssc_percentage=form.ssc_percentage.data
            attempted_user1.ssc_institute=form.ssc_institute.data
            attempted_user1.ssc_pyr=form.ssc_pyr.data
            attempted_user1.ssc_state=form.ssc_state.data
            attempted_user1.ssc_city=form.ssc_city.data
            attempted_user1.skill=form.skill.data
            attempted_user1.achievements=form.achievements.data
            attempted_user1.previous_projects=form.previous_projects.data
            attempted_user1.git_url=form.git_url.data
            attempted_user1.hobby=form.hobby.data
            attempted_user1.work_exp=form.work_exp.data
            db.session.add(attempted_user1)
            db.session.commit()
            flash('Details updated sucessfully',category='success')
            time.sleep(2)
            return redirect(url_for('studentprofile'))
            
        else:
            # if attempted_user1:
            #     db.session.delete(attempted_user1)
            #     db.session.commit()
    
            student=Sadditional(
                    username=attempted_user.username,
                    dob=form.dob.data,
                    gender=form.gender.data,
                    state=form.state.data,
                    city=form.city.data,
                    address=form.address.data,
                    pin_code=form.pin_code.data,
                    g_course=form.g_course.data,
                    g_percentage=form.g_percentage.data,
                    g_institute=form.g_institute.data,
                    g_yr=form.g_yr.data,
                    g_state=form.g_state.data,
                    g_city=form.g_city.data,
                    hd_class=form.hd_class.data,
                    hd_percentage=form.hd_percentage.data,
                    hd_institute=form.hd_institute.data,
                    hd_pyr=form.hd_pyr.data,
                    hd_state=form.hd_state.data,
                    hd_city=form.hd_city.data,
                    ssc_class=form.ssc_class.data,
                    ssc_percentage=form.ssc_percentage.data,
                    ssc_institute=form.ssc_institute.data,
                    ssc_pyr=form.ssc_pyr.data,
                    ssc_state=form.ssc_state.data,
                    ssc_city=form.ssc_city.data,
                    skill=form.skill.data,
                    achievements=form.achievements.data,
                    previous_projects=form.previous_projects.data,
                    git_url=form.git_url.data,
                    hobby=form.hobby.data,
                    work_exp=form.work_exp.data
                )
            db.session.add(student)
            db.session.commit()
            flash('Details updated sucessfully',category='success')
            return redirect(url_for('studentprofile'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'there was error: {err_msg}')
    if attempted_user1:
        return render_template("student editprofile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,form=form)
    else:
        return render_template("student editprofile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,form=form)
#, lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,dob=dob,gender=gender,state=state,city=city,address=address,pin_code=pin_code,g_course=g_course,g_percentage=g_percentage,g_institute=g_institute,g_yr=g_yr,g_state=g_state,g_city=g_city,hd_class=hd_class,hd_percentage=hd_percentage,hd_institute=hd_institute,hd_pyr=hd_pyr,hd_state=hd_state,hd_city=hd_city,ssc_class=ssc_class,ssc_percentage=ssc_percentage,ssc_institute=ssc_institute,ssc_pyr=ssc_pyr,ssc_state=ssc_state,ssc_city=ssc_city,skill=skill,achievements=achievements,previous_projects=previous_projects,git_url=git_url,hobby=hobby,work_exp=work_exp,
#, lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address

@app.route("/upload resume",methods=['POST','GET'])
def uploadresume():
    form = resumeform()
    txt_resume=""
    user=session.get('user', None)
    attempted_user = Sadditional.query.filter_by(username=user).first() #used first to grab the data
    if attempted_user:
        txt_presume=attempted_user.txt_presume
    if form.validate_on_submit() and request.method=='POST':
        file=form.resume_pdf.data
        
        attempted_user = Sadditional.query.filter_by(username=user).first() #used first to grab the data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        attempted_user.presume=file.read()
        attempted_user.txt_presume=file.filename
        db.session.add(attempted_user)
        db.session.commit()
        # rendered = render_template("")
        # pdf = pdfkit.from_string(rendered,False)
        # response = make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'inline;filename=output.pdf'
        return render_template("upload resume.html",form=form,filename=txt_presume)
        #return send_file(BytesIO(attempted_user.presume),attachment_filename=file.filename, as_attachment=True)
    return render_template("upload resume.html",form=form,filename=txt_presume)


@app.route("/apply for job",methods=['POST','GET'])
def applyforjob():
    form = applied_form()
    jobs = Jobs.query.all()
    user=session.get('user', None)
    attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    attempted_user1 = Sadditional.query.filter_by(username=user).first() #used first to grab the data
    applied1 = Approved_students.query.filter_by(cposition=form.value1.data, cname=form.value.data, fname=attempted_user.fname, email_address=attempted_user.email_address).first()
    if form.validate_on_submit() and request.method=='POST':
        if attempted_user and attempted_user1 and not applied1:
            applied=Approved_students(
                    cname = form.value.data,
                    cposition = form.value1.data,
                    cstatus = "Pending",
                    email_address = attempted_user.email_address,
                    phone_no = attempted_user.phone_no,
                    lname = attempted_user.lname,
                    fname = attempted_user.fname,
                    mname = attempted_user.mname,
                    dob = attempted_user1.dob,
                    gender = attempted_user1.gender,
                    state = attempted_user1.state,
                    city = attempted_user1.city,
                    address = attempted_user1.address,
                    pin_code = attempted_user1.pin_code,
                    g_course = attempted_user1.g_course,
                    g_percentage = attempted_user1.g_percentage,
                    g_institute = attempted_user1.g_institute,
                    skill = attempted_user1.skill,
                    txt_resume = attempted_user1.txt_presume
                )
            if applied1:
                form.apply.data="Applied"
            db.session.add(applied)
            db.session.commit()
            return redirect(url_for('studentpastapplications'))
                
    return render_template("apply for job.html",jobs=jobs,form=form)

@app.route("/student past applications")
def studentpastapplications():
    jobs = Jobs.query.all()
    user=session.get('user', None)
    attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    applied1 = Approved_students.query.filter_by(fname=attempted_user.fname, email_address=attempted_user.email_address).all()
    #applied = Approved_students.query.all()
    data=[]
    if applied1:
        # data = db.session.query(applied, jobs)\
        # .filter(jobs.cname==applied.cname,jobs.cposition==applied.cposition)\
        # .join(applied, jobs.cname == applied.cname, jobs.cposition == applied.cposition)\
        # .all()
        for apply in applied1:
            job = Jobs.query.filter_by(cname=apply.cname, cposition=apply.cposition).first()
            if job:
                sdata=dict()
                sdata["cname"]=job.cname
                sdata["cstatus"]=apply.cstatus
                sdata["ccity"]=job.ccity
                sdata["cstate"]=job.cstate
                sdata["caddress"]=job.caddress
                sdata["cqualification"]=job.cqualification
                sdata["cposition"]=job.cposition
                sdata["csalary"]=job.csalary
                sdata["cdesc"]=job.cdesc
                data.append(sdata)
                
    
    return render_template("student past applications.html",data = data)

@app.route("/recruiter edit profile",methods=['POST','GET'])
def recruitereditprofile():
    form=Radditionalform()
    recruiter=session.get('user', None)
    attempted_user = Recruiter.query.filter_by(username=recruiter).first() #used first to grab the data
    if attempted_user:
        lname=attempted_user.lname
        fname=attempted_user.fname
        mname=attempted_user.mname
        phone_no=attempted_user.phone_no
        email_address=attempted_user.email_address
    
    attempted_recruit = Radditional.query.filter_by(username=recruiter).first()
    
    if attempted_recruit:
        cname = attempted_recruit.cname
        cstate = attempted_recruit.cstate
        ccity = attempted_recruit.ccity
        caddress = attempted_recruit.caddress
        cpin_code = attempted_recruit.cpin_code
    
    if form.validate_on_submit() and request.method=='POST':
        if attempted_recruit:
            attempted_recruit.cname=form.nameofc.data
            attempted_recruit.cstate=form.state.data
            attempted_recruit.ccity = form.city.data
            attempted_recruit.caddress = form.address.data
            attempted_recruit.cpin_code = form.pin_code.data
            db.session.add(attempted_recruit)
            db.session.commit()
            return redirect(url_for('recruiterprofile'))
            
        else:
            attempted_recruiter = Radditional(
                    username = recruiter,
                    cname = form.nameofc.data,
                    cstate = form.state.data,
                    ccity = form.city.data,
                    caddress = form.address.data,
                    cpin_code = form.pin_code.data
                )
            db.session.add(attempted_recruiter)
            db.session.commit()
            return redirect(url_for('recruiterprofile'))
        
    if attempted_recruit:
        return render_template("recruiter edit profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,cname = cname,cstate = cstate,ccity = ccity,caddress = caddress,cpin_code = cpin_code,form=form)
    else:
        return render_template("recruiter edit profile.html", lname=lname, fname=fname, mname=mname, phone_no=phone_no, email_address=email_address,form=form)

@app.route("/recruiter job applications",methods=['POST','GET'])
def recruiterjobapplications():
    form = Jobform()
    recruiter=session.get('user', None)
    attempted_recruit = Radditional.query.filter_by(username=recruiter).first()
    if form.validate_on_submit() and request.method=='POST':
        if attempted_recruit:
            job = Jobs(
                    username = attempted_recruit.username,
                    cname = attempted_recruit.cname,
                    ccity = attempted_recruit.ccity,
                    cstate = attempted_recruit.cstate,
                    caddress = attempted_recruit.caddress,
                    cqualification = form.cqualification.data,
                    cposition = form.cposition.data,
                    csalary = form.csalary.data,
                    cdesc = form.cdesc.data
                )
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('recruiterjobapplications'))
    
    
    if attempted_recruit:
        cname = attempted_recruit.cname
        cstate = attempted_recruit.cstate
        ccity = attempted_recruit.ccity
        caddress = attempted_recruit.caddress
        cpin_code = attempted_recruit.cpin_code
        
    if attempted_recruit:
        return render_template("recruiter job applications.html",cname = cname,cstate = cstate,ccity = ccity,caddress = caddress,cpin_code = cpin_code,form=form)
    else:
        return render_template("recruiter job applications.html",form=form)

@app.route("/recruiter send approval",methods=['POST','GET'])
def recruitersendapproval():
    form = send_approval()
    recruiter=session.get('user', None)
    
    attempted_user = Radditional.query.filter_by(username=recruiter).first() #used first to grab the data
    if attempted_user:
        applied1 = Approved_students.query.filter_by(cname=attempted_user.cname).all()
    
    if form.validate_on_submit() and request.method=='POST':
        if form.download.data:
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename=form.txt_resume.data, as_attachment=True)
            
        elif form.approve.data:
            applied1 = Approved_students.query.filter_by(cname=attempted_user.cname,cposition=form.position.data,txt_resume=form.txt_resume.data).first()
            applied1.cstatus = "Approved"
            db.session.add(applied1)
            db.session.commit()
            return redirect(url_for('recruitersendapproval'))
    #attempted_user = User.query.filter_by(username=user).first() #used first to grab the data
    #attempted_user1 = Sadditional.query.filter_by(username=user).first() #used first to grab the data
        
    return render_template("recruiter send approval.html",applied1=applied1,form=form)

@app.route("/recruiter past approval")
def recruiterpastapproval():
    recruiter=session.get('user', None)
    
    attempted_user = Radditional.query.filter_by(username=recruiter).first() #used first to grab the data
    if attempted_user:
        applied1 = Approved_students.query.filter_by(cname=attempted_user.cname).all()
        
    return render_template("recruiter past approval.html",applied1=applied1)

@app.route("/logout")
def logoutuser():
    logout_user()
    #session.pop('user')
    flash("You have been logged out!",category="info")
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)
'''

<form action="{{ url_for('uploadresume') }}" method="post" enctype="multipart/form-data">
                {{ form.csrf_token }}
                {{ form.hidden_tag() }}
                <div class="form-row">
                    <div class="input-group input-group-lg">
                        {{ form.resume_pdf(class="form-file form-control", value=gender) }}
                        
                        <a href="#" class="btn2 btn-outline-dark btn btn-lg active"
                            role="button" id="inputGroupFileAddon04">Upload</button></a>
                    </div>
                </div>
                <div class="form-row">
                    {{ form.submit(class="btn1 mt-3 mb-4 btn-primary") }}
                    <div class="col-lg-5">
                        <a href="{{ url_for('studentprofile') }}" class="btn1 mt-3 mb-4 btn btn-white btn-lg active"
                            role="button" aria-pressed="true">Save</a>
                    </div>
            </form>
'''