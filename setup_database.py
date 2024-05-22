from app import app, db
from models import User

with app.app_context():
    """
    This script sets up the database and creates the necessary tables.
    """

    db.create_all()
    print("Database and tables created.")
