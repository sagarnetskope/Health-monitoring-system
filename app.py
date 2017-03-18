from flask import Flask,render_template,session,request,redirect,url_for,g
from flask_bootstrap import Bootstrap
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

Bootstrap(app)

@app.route('/home',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return "in signup page"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form['password']=='password'#fetch from database for user
            session['user']=request.form['username']
            redirect(url_for('user_info'))
            #return "login successfull"

@app.route('/user_info',methods=['GET','POST'])
def user_info():
    if request.method=='GET':
        return render_template('user_info.html')
    else if request.method=='POST':
        #get user information and push it to database

@app.route('/about')
def about():
    return "about page"

@app.route('/contact')
def contact():
    return "contact page"

@app.before_request
def Check_session():
    g.user=None
    if user in session:
        g.user=session['user']
    else:
        return "not logged in"
@app.route('/dropsession')
def drop_session():
    session.pop('user',None)
    return "Session Dropped"

if __name__=='__main__':
    app.run(debug=True,port=9000)


