from flask import current_app as app, jsonify, request, render_template
from flask_security import auth_required, roles_required
from application.models import db, User, Role
from application.sec import datastore
from werkzeug.security import check_password_hash

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/librarian')
@auth_required("token")
@roles_required("librarian")
def librarian():
    return "Welcome Librarian"

@app.get('/librarian/user/<int:user_id>')
@auth_required("token")
@roles_required("librarian")
def librarian_activate(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.active = True
    db.session.commit()
    return jsonify({"message": "User Activated Successfully"})

@app.post('/user-login')
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username or password not provided"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password_hash, password):
        # Assuming you have a method to generate token for authenticated users
        token = user.get_auth_token()  # Ensure you have implemented this method in your User model
        return jsonify({"token": token, "username": user.username, "role": user.role.name})
    else:
        return jsonify({"message": "Wrong Password"}), 400
