from fake_pinterest import database, app
from fake_pinterest.models import User, Posts


with app.app_context():
    database.create_all()