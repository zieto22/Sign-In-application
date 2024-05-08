from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

def savedUser(username, password):
   with open('userfile.txt', 'a') as f:
        f.write(f"{username}:{password}\n")

def get_user(username):
    with open('userfile.txt', 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username:
                return stored_password
    return None

def log(username, password):
    with open('userfile.txt', 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username and stored_password == password:
                return True
    return False   

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        print(username, password)

        # Print the contents of the userfile.txt for debugging
        savedUser(username, password)
        with open('userfile.txt', 'r') as f:
            print("Contents of userfile.txt:")
            print(f.read())

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    print("Request Form:", request.form)
    username = request.form['username']
    password = request.form['password']

    if username is None or password is None:
        return 'Missing username or password'

    if log(username, password):
        return 'Login successful!'
    else:
        return render_template('index.html', alert_message="Invalid username or password")

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

