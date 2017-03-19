from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Email,Length
from wtforms import StringField,PasswordField
from flask_login import UserMixin,LoginManager
from werkzeug.security import check_password_hash,generate_password_hash
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/nsadmin/contacts.db'

Bootstrap(app)
db=SQLAlchemy(app)


class User(db.Model,UserMixin):
    user_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(80))
    #add more things here



class SignupForm(FlaskForm):
    #add other fields
    username=StringField('username',validators=[Email(message='Please enter valid email')])
    password=PasswordField('password',validators=[Length(min=8,max=80,message='Length of password must be between 8 to 80 letters')])

login_manager=LoginManager()
login_manager.init_app(app)

#@login_manager.user_loader()
#def Load_user(user_id):
  #  return User.query.get('user_id')



@app.route('/home',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        #return 'form submitted and validated'
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        #add error message for unique username
        new_user=User(username=form.username.data,password=hashed_password)#creating an object for sqlalchemy
        db.session.add(new_user)#add new user to database
        db.session.commit()
        return redirect(url_for('index'))#redirect to index.html
    return render_template('signup.html',form=form)


@app.route('/login',methods=['POST'])
def login():
    user=User.query.filter_by(username=request.form['username']).first()
    if user:
            if check_password_hash(user.password,request.form['password']):
                return redirect(url_for('user_info'))
            else:
                return "login not successfull"



@app.route('/user_info',methods=['GET','POST'])
def user_info():
  if request.method=='GET':
        return render_template('user_info.html')
 #   else if request.method=='POST':
        #get user information and push it to database

@app.route('/about')
def about():
    return "about page"

@app.route('/contact')
def contact():
    return "contact page"



if __name__=='__main__':
    app.run(debug=True,port=9000)


