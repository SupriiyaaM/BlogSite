from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')









'''from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1 ,type=int) #query parameter, default value and type
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page= 5) # newest post first (desc); pagination 
    return render_template('home.html',  posts = posts, title='BlogVille') 

#arguement passed in template;
#second post arguement is equal to the actual posts


@main.route("/about")
def about():
    return render_template('about.html', title='About') 
'''
