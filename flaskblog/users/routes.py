from flask import Blueprint
from flask import render_template, url_for , flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flask import current_app
from flaskblog.models import User, Post
from flaskblog.users.forms import (Registrationform, Loginform, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
import os

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET','POST'])
def register():
     if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
#now we create instance of out form that we send to our application; then we can pass 'form' to a template
     form = Registrationform()
     if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user = User( username =form.username.data, email = form.email.data, password = hashed_password )
         db.session.add(user)
         db.session.commit() #when input from form; commmited to database and retrieved with query
         flash(f'Account created for {form.username.data}!, you are now able to Login.', 'success')
         return redirect(url_for('users.login')) #name of function ; login
     return render_template('register.html', title='Register', form=form)
 
 

@users.route("/login",  methods=['GET','POST'] )
def login():
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
#now we create instance of out form that we send to our application; then we can pass 'form' to a template
     form = Loginform()
     if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data): #database and form password check
             login_user(user,remember=form.remember.data)
             next_page = request.args.get('next') #if account does not exists (not logged_in) value true
             return redirect (next_page) if next_page else redirect(url_for('main.home'))
        else:
             flash(f'Login Unsuccessful. Please check email and password.', 'danger')       
     return render_template('login.html', title='Login', form=form)
 
 
 
@users.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account",  methods=['GET','POST'] )
@login_required
def account():    
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: #if picture data was inserted manually; different section of code
            old_pic = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #updating from default to uploaded
            if old_pic != 'default.jpeg':
                os.remove(os.path.join(current_app.root_path, 'static/profile_pics', old_pic))
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account information has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET': #populate form with current information
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
 
 
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username = username).first_or_404() #getting the user
    posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page= 5)  #filter by the user who is the author of the posts
    return render_template('user_posts.html',  posts = posts, user = user) 


@users.route("/reset_password",  methods=['GET','POST'])
def reset_request(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) #user has to be logged out
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() #now we need to send the email; get the user
        send_reset_email(user)
        flash('An email has been send with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form ) 


@users.route("/reset_password/,<token>",  methods=['GET','POST'])
def reset_token(token): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    user = User.verify_reset_token(token) #created in models; if we don't get user back; expired or invalid
    if user is None:
        flash('That token is invalid or expired', 'warning')
        return redirect (('users.reset_request')) 
    form = ResetPasswordForm()
    if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user.password = hashed_password
         db.session.commit() 
         flash('Your Password has been updated! You are now able to log in.', 'success')
         return redirect(url_for('users.login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form )     