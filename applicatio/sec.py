from flask_security import Security, SQLAlchemyUserDatastore
from .models import db, User, Role

# Custom User Datastore
class CustomUserDatastore(SQLAlchemyUserDatastore):
    def __init__(self, db, user_model, role_model):
        super().__init__(db, user_model, role_model)

datastore = CustomUserDatastore(db, User, Role)

# Flask-Security Setup
security = Security(datastore)

# Initialize Flask-Security with app and datastore
def setup_security(app):
    security.init_app(app, datastore)
