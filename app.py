from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Email,Length
from wtforms import StringField,PasswordField
from flask_login import UserMixin,LoginManager,login_required,login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_mail import Mail,Message
#from flask import flash
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/nsadmin/contacts.db'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'health.monitoring2017@gmail.com'
app.config['MAIL_PASSWORD'] = 'sagar123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

Bootstrap(app)
db=SQLAlchemy(app)


class User(db.Model,UserMixin):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(80))
    #add more things here


    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.email = email
        #self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.username)



class SignupForm(FlaskForm):
    #add other fields
    username=StringField('username',validators=[Email(message='Please enter valid email')])
    password=PasswordField('password',validators=[Length(min=8,max=80,message='Length of password must be between 8 to 80 letters')])

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    #print '\n\n\n In user_loader function \n\n and returned value is'+str(User.get(unicode(user_id)))+'\n\n\n'
    return User.query.get(int(user_id))



@app.route('/home',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        #return 'form submitted and validated'
        hashed_password=generate_password_hash(form.password.data)
        #add error message for unique username
        new_user=User(username=form.username.data,password=hashed_password)#creating an object for sqlalchemy
        db.session.add(new_user)#add new user to database
        db.session.commit()
        msg=Message('You have successfully signed up to HMS',sender='health.monitoring2017@gmail.com',recipients=['tanay@netskope.com','sags.sharma@gmail.com','saikiran@netskope.com'])
        mail.send(msg)
       # flash("Successfully signed in",'success')
        return redirect(url_for('index'))#redirect to index.html
    return render_template('signup.html',form=form)


@app.route('/login',methods=['POST'])
def login():
    #print '\n\n\ninside login route and authetication will be done after this\n\n\n'
    user=User.query.filter_by(username=request.form['username']).first()
    #print "\n\nusername from form  is "+request.form['username']
    #print "username from database is \n\n"+user.username
    if user:
            if check_password_hash(user.password,request.form['password']):
                #print '\n\n\nuser is\n\n'+str(user)+'\n\n\n'
                #print "\n\n user.user_id"+str(user.user_id)+'\n\n\n'
                login_user(user)
                return redirect(url_for('user_info'))
            else:
                return "login not successfull Password is incorrect"
    else:
        "Login not successful ie username is incorrect"



@app.route('/user_info',methods=['GET','POST'])
@login_required
def user_info():
    #flash('logging IN')
    if request.method=='GET':
        return render_template('user_info.html')
 #   else if request.method=='POST':
        #get user information and push it to database

@app.route('/about')
def about():
    return "about page"

@app.route('/contact')
def contact():
    return render_template('contacts.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.html'))



if __name__=='__main__':
    app.run(debug=True,port=9000)


