import os #grabs extension from the image file that user has uploaded
import secrets #hex
from PIL import Image
from flask import url_for
from flask_mail import Message #for mail
from flaskblog import  mail
from flask import current_app



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #we don't want the file name of uploaded picture as it might colide with a picture file already in our folder; randomize image name (hex)    
    f_name, f_ext = os.path.splitext(form_picture.filename)
    #make sure extension is preserved; file name for picture uploaded; import os module; returns file name w and w/o extension
    picture_fn = random_hex + f_ext
    #filename = extension + hex; path to where image is saved
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #saving the picture
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', 
                  sender= current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True) }
    
If you did not make this request then simply ignore this email and no changes will be made.      
'''
    mail.send(msg)
