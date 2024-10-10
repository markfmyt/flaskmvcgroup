from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        try:
            db.session.commit()
            return True  # Return True on successful commit
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return None  # Return None if there was an error
    return None

def create_user(username, password, email, role):
    hashed_password = generate_password_hash(password)
    user = None

    if role == 'employer':
        user = Employer(username=username, password=hashed_password, email=email)
    elif role == 'job_seeker':
        user = JobSeeker(username=username, password=hashed_password, email=email)
    elif role == 'admin':
        user = Admin(username=username, password=hashed_password, email=email)
    
    if user:
        db.session.add(user)
        try:
            db.session.commit()  # Attempt to commit the session
            return True  # Return True on successful commit
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return None  # Return None if there was an error
    
    return None

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return access_token
    
    return None

def get_all_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.__class__.__name__
        })
    return users_list
