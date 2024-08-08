from main import app
from application.models import db, User, Role
from application.sec import datastore
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Create roles if they don't exist
    if not Role.query.filter_by(name="librarian").first():
        db.session.add(Role(name="librarian", description="User is a Librarian"))
    
    if not Role.query.filter_by(name="User").first():
        db.session.add(Role(name="User", description="User - an individual who wants to access an e-book from the library"))
    
    db.session.commit()

    # Retrieve roles
    librarian_role = Role.query.filter_by(name="librarian").first()
    user_role = Role.query.filter_by(name="User").first()

    # Create users if they don't exist
    if not User.query.filter_by(username="lib").first():
        db.session.add(User(
            username="lib",
            password_hash=generate_password_hash("librarian"),
            fs_uniquifier="lib_unique_id",  # Example unique identifier
            role_id=librarian_role.id,
            active=True  # Set user as active
        ))
    
    if not User.query.filter_by(username="user1").first():
        db.session.add(User(
            username="user1",
            password_hash=generate_password_hash("user1"),
            fs_uniquifier="user1_unique_id",  # Example unique identifier
            role_id=user_role.id,
            created_at=db.func.current_timestamp(),  # Set created_at timestamp
            updated_at=db.func.current_timestamp(),  # Set updated_at timestamp
            active=True  # Set user as active
        ))

    # Commit changes to the database
    db.session.commit()

    print("Initial data setup complete.")
