from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # fl: profile pic updation
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user #to check while updating if new username and email are available
from flaskblog.models import User


class Registrationform(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max= 20)])
        #list of validations that need to be checked; passed as an arugement; also imported classes
    email = StringField('Email',validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('confirm_password', validators = [DataRequired(), EqualTo('password')])
    submit =  SubmitField('Sign Up')
    
    def validate_username (self, username) :
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
        
    def validate_email (self, email) :
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email is already taken. Please choose a different one.')
    
     
class Loginform(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit =  SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max= 20)])
    email = StringField('Email',validators = [DataRequired(), Email()])
    picture =FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit =  SubmitField('Update Information')
    
    def validate_username (self, username) :
        if username.data != current_user.username : #validate only if username and email updated are new values
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')
        
    def validate_email (self, email) :
        if email.data != current_user.email :
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email is already taken. Please choose a different one.')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(), Email()])   
    submit = SubmitField('Request Password Reset')   
    def validate_email (self, email) :
        # if email.data != current_user.email :
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There exists no account with this email. Kindly register first.')  
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('confirm_password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')                    