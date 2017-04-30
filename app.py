from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Email,Length,EqualTo,NumberRange
from wtforms import StringField,PasswordField,IntegerField,FloatField
from flask_login import UserMixin,LoginManager,login_required,login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_mail import Mail,Message
from sqlalchemy.exc import IntegrityError
#from datadog import statsd
#import time

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
    name=db.Column(db.String(20))
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(80))
    #add more things here


    def __init__(self,name, username, password):
        self.name=name
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

class Contact(db.Model, UserMixin):
        __tablename__ = "contact"
        c_id=db.Column(db.Integer,primary_key=True)
        c_name = db.Column(db.String(20))
        c_email= db.Column(db.String(20), unique=True)
        c_mobile = db.Column(db.String(20))
        c_message= db.Column(db.String(80))

        # add more things here


        def __init__(self, name,email, message,mobile):
            self.c_name = name
            self.c_email = email
            self.c_message = message
            self.c_mobile = mobile
            # self.registered_on = datetime.utcnow()

        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            return unicode(self.user_id)

        def __repr__(self):
            return '<User %r>' % (self.c_name)


class User_info(db.Model, UserMixin):
    __tablename__ = "user_info"
    u_name = db.Column(db.String, primary_key=True)
    u_age = db.Column(db.String(20))
    u_height = db.Column(db.String(20))
    u_weight = db.Column(db.String(20))
    u_bmi = db.Column(db.String(20))

    # add more things here


    def __init__(self, name, age, height,weight,bmi):
        self.u_name = name
        self.u_age = age
        self.u_height= height
        self.u_weight = weight
        self.u_bmi=bmi
        # self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


    def __repr__(self):
        return '<User %r>' % (self.u_name)


class SignupForm(FlaskForm):
    name = StringField('Name')
    username=StringField('username',validators=[Email(message='Please enter valid email')])

    password=PasswordField('password',validators=[InputRequired(message='Enter a password'),Length(min=8,max=80,message='Length of password must be between 8 to 80 letters'),EqualTo('confirmPassword',message='Passwords must match')])
    confirmPassword=PasswordField('confirm Password', validators=[Length(min=8, max=80, message='Length of password must be between 8 to 80 letters')])



login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    #print '\n\n\n In user_loader function \n\n and returned value is'+str(User.get(unicode(user_id)))+'\n\n\n'
    return User.query.get(int(user_id))



@app.route('/home',methods=['GET','POST'])
def index():
    #start=time.time()
    if request.method=='GET':
        return render_template('index.html',my_error='')
    if request.method=='POST':
        new_contact= Contact(name=request.form['name'], email=request.form['email'],message=request.form['message'],mobile=str(request.form['mobile']))  # creating an object for sqlalchemy#add more things
        db.session.add(new_contact)  # add new contact to database
        db.session.commit()
        # statsd.histogram('contact_Database_submit_time',time.time()-start)
        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        message=request.form['message']
        bdy='\n\n customer name :'+name+'\n\ncontact no : '+str(mobile)+'\n\n message : '+message
        msg = Message(subject='Your customer  wants to contact with you',body=bdy,sender='health.monitoring2017@gmail.com', recipients=['sags.sharma@gmail.com','sagar@netskope.com'])
        mail.send(msg)
     #   statsd.histogram('Mail_send_time',time.time()-start)
        return render_template('index.html',my_error='')

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=SignupForm()
    try:
        if form.validate_on_submit():
        #return 'form submitted and validated'
            hashed_password=generate_password_hash(form.password.data)
        #add error message for unique username
            new_user=User(name=form.name.data,username=form.username.data,password=hashed_password)#creating an object for sqlalchemy#add more things
            db.session.add(new_user)#add new user to database
            db.session.commit()
            msg=Message(subject='You have successfully signed up to Health Monitoring System',body='Complete your registration by going to This url\nhttp://localhost:9000/home',sender='health.monitoring2017@gmail.com',recipients=[form.username.data])
            mail.send(msg)
       # flash("Successfully signed in",'success')
            return redirect(url_for('index'))#redirect to index.html
    except IntegrityError as err:
            db.session.rollback()
            if "UNIQUE constraint failed: user.username" in str(err):
                my_error=" Username already exists %s" % form.username.data
                return render_template('signup.html',form=form,my_error=my_error)
            elif "FOREIGN KEY constraint failed" in str(err):
                return "supplier does not exist"
            else:
                return "unknown error adding user"
    return render_template('signup.html',form=form)


@app.route('/login',methods=['POST'])
def login():
    #s=time.time()
    #print '\n\n\ninside login route and authetication will be done after this\n\n\n'
    user=User.query.filter_by(username=request.form['username']).first()
    #print "\n\nusername from form  is "+request.form['username']
    #print "username from database is \n\n"+user.username
    #statsd.histogram('query_time',time.time()-s)
    if user:
            if check_password_hash(user.password,request.form['password']):
                name=user.name
                #print '\n\n\nuser is\n\n'+str(user)+'\n\n\n'
                #print "\n\n user.user_id"+str(user.user_id)+'\n\n\n'
                login_user(user)
                return redirect(url_for('user_info',user=name))
            else:
                error='Please Enter Correct Password'
                return render_template('index.html',my_error=error)
    else:
        error='Please Enter Correct Username OR SignUp First'
        return render_template('index.html',my_error=error)


name=''
@app.route('/user_info',methods=['GET','POST'])
@login_required
def user_info():
    if request.method=='GET':
        global name
        name= request.args.get('user')
        return render_template('user_info.html',myvar=name,func=Bmi_calculator)
    if request.method=='POST':
        height=request.form['height']
        weight=request.form['weight']
        bmi=Bmi_calculator(weight,height)
        global name
        x=name
        new_user_info = User_info(name=x, age=str(request.form['age']), height=str(height),weight=str(weight),bmi=str(bmi))  # creating an object for sqlalchemy#add more things
        db.session.add(new_user_info)  # add new contact to database
        db.session.commit()
        return render_template('bmi.html',myvar=bmi)
        #return "<h1>validated</h1>"



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi_entry.html')

@app.route('/contacts')
def contact():
    return render_template('contacts.html')

@app.route('/guide')
def Guide():
    return render_template('guide.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/maps')
def maps():
    return render_template('maps.html')

def Bmi_calculator(weight,height):
   # s=time.time()
    height=float(height)
    weight=float(weight)
    x=float(height**2)
    bmi=(weight/x)*703
    #statsd.histogram('bmi_caal_time',time.time()-s)
    return bmi



if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
