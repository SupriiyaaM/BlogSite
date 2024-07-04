from flaskblog import db, login_manager 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):  #function for getting user by id
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin): #import from db.Model
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key= True ) 
    username = db.Column(db.String(20), unique= True, nullable= False)
    email = db.Column(db.String(120), unique= True, nullable= False)  
    image_file = db.Column(db.String(120), nullable= False, default = 'default.jpeg') #hashing for length
    password = db.Column(db.String(60), nullable= False)
    posts = db.relationship ('Post', backref = 'author', lazy =  True) #one-to-many relationship; backref: author attribute to get user of post ; lazy: loads in one go
    
    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')
    
    
    @staticmethod #self parameter not arguement, only token
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] #loads token
        except:
            return None
        return User.query.get(user_id)    #returns user with user_id    
  
    def __repr__(self): # how user object is printed 
        return f"User('{self.username}', '{self.email}' ,'{self.image_file}')"
    
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key= True ) 
    title = db.Column(db.String(100), nullable= False)
    date_posted= db.Column(db.DateTime, nullable= False, default= datetime.utcnow ) # no (): function as arguement; not current time
    content = db.Column(db.Text, nullable= False)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable = False) #lowercase user not class; table and column name
    
    def __repr__(self): # how post object is printed 
        return f"Post('{self.title}', '{self.date_posted}')"
