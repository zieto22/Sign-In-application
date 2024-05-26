# setup_database.py
from app import app, db
from models import User, Todo

with app.app_context():
    db.create_all()
    print("Database and tables created.")
