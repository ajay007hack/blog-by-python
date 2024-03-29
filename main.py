from flask import Flask , render_template ,request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
import json
from flask_mail import Mail


with open('config.json' , 'r') as c:
    params = json.load(c) ["params"]

app = Flask(__name__ , template_folder= 'template')

app.config.update(


    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-pass']

)
mail = Mail(app)

local_server = True
if (local_server) :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']



db = SQLAlchemy(app)


class Contacts(db.Model):
    '''serial no , name ,phone ,msg, date,email'''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)

    msg = db.Column(db.String(120), primary_key=False)
    date = db.Column(db.String(12) , nullable=True)
    email = db.Column(db.String(120),  nullable=False)


class Posts(db.Model):
    '''serial no , name ,phone ,msg, date,email'''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(12),  nullable=False)

    content= db.Column(db.String(120), primary_key=False)
    date = db.Column(db.String(12) , nullable=True)
    tagline = db.Column(db.String(12) , nullable=True)


@app.route("/dash") 
def dashboard():
    return render_template('dashboard.html', params = params)





@app.route("/")
def Home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]

    return render_template('index.html', params = params , posts = posts)
@app.route("/about") 
def about():
    return render_template('about.html', params = params)
@app.route("/contact", methods = ['GET','POST'])
def contact():
    if (request.method == 'POST'):

        '''add entry from the database'''
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        entry = Contacts(name = name, phone_num= phone , msg = message , date = datetime.now() ,email = email)
        db.session.add(entry)
        db.session.commit()


        mail.send_message('New message from'+ name,
                           sender = email,
                           recipients = [params['gmail-user']],
                           body = message + "\n" + phone
                         )
    return render_template('contact.html' , params = params)
#@app.route("/sample post/<string:post_slug>", methods = ['GET'])
@app.route("/sample_post/<string:post_slug>", methods = ['GET'])
def posts_sample(post_slug):
    post= Posts.query.filter_by(slug = post_slug).first()
    return render_template('posts.html' , params = params , post = post )    

app.run(debug=True)    
  