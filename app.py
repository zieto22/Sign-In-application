# app.py
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import TodoForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """Represents a user in the application."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Todo(db.Model):
    """Represents a todo item in the application."""
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! Redirecting to login page', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for('todo_list'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/todos', methods=['GET', 'POST'])
def todo_list():
    """Renders the todo list page and handles todo creation."""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(
            description=form.description.data,
            completed=False,
            user_id=user_id
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo_list'))
    todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('todos.html', todos=todos, form=form)

@app.route('/todo/<int:todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    """Handles marking a todo as completed or not completed."""
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect(url_for('todo_list'))

@app.route('/todo/<int:todo_id>/delete', methods=['POST'])
def delete_todo(todo_id):
    """Handles deleting a todo."""
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('todo_list'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
