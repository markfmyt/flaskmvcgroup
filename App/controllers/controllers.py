from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify

# Controller function to initialize the database
def initialize():
    db.drop_all()
    db.create_all()
    
    return f"Database initialized."

'''
User Controllers
'''


'''
Job Controllers
'''


'''
Employer Controllers
'''

def get_user_by_id(user_id):
    return User.query.get(user_id)

'''
Admin Controllers
'''
