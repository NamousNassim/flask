from flask import redirect, url_for, Blueprint , render_template , request , flash 
from .models import User
from . import db 
from flask_login import login_user , login_required , logout_user , current_user
from werkzeug.security import generate_password_hash , check_password_hash
auth = Blueprint('auth', __name__)

@auth.route("/login" , methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first() 
        if user: 
            if check_password_hash(user.password, password):
                flash("connected ! " , category='success')
                login_user(user,remember=True)
                redirect(url_for('views.home'))
            else: 
                flash("incorrect password" , category='error')
        
        else: 
            flash("username incorecct" , category='error')


    return render_template("login.html" ,  user = current_user)

@auth.route("/logout")
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

 

@auth.route("/sign_up" , methods=['GET','POST'])
def sign_up(): 
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get("username")
        password = request.form.get("password")
        password1 = request.form.get("password1")

        user = User.query.filter_by(email=email).first()

        if user: 
            flash("email already exists " , category='error')

        user_name= User.query.filter_by(username=username).first()
        if user_name:
            flash ("username already taken " , category='error') 
        


        if len(email) < 4:
            flash("email must be good bro " , category='error')
        elif len(username) < 2: 
            flash("invalid firstaname " , category='error')
        elif password != password1:
            flash("password does not match " , category='error')
        elif len(password) < 7:
            flash("password weak " , category="error")
      
        else:
            new_user = User(email=email,username=username,password=generate_password_hash(password , method='pbkdf2:sha256'))
            flash("account created ! ", category='succes')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))
    return render_template('sign_up.html' , user=current_user)