from flask import Blueprint, render_template, jsonify, request
from App.controllers import *
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application

everyone_views = Blueprint('everyone_views', __name__, template_folder='../templates')

@everyone_views.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# User Login
@everyone_views.route('/api/users/login', methods=['POST'])
def login_user_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    return login_user(username, password)

# User Signup
@everyone_views.route('/api/users/signup', methods=['POST'])
def signup_user_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    return create_user(username, password, email, role)

# Job Postings
@everyone_views.route('/api/jobs', methods=['GET'])
def list_jobs_api():
    return get_all_jobs()

@everyone_views.route('/api/users/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import get_user_by_id

# Dashboard Route
@everyone_views.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    # Redirect to different dashboards based on role
    if user.role == 'admin':
        return admin_dashboard()
    elif user.role == 'jobseeker':
        return jobseeker_dashboard()
    elif user.role == 'employer':
        return employer_dashboard()
    else:
        return render_template('error.html', message="Invalid Role")

# Admin Dashboard
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Jobseeker Dashboard
def jobseeker_dashboard():
    return render_template('jobseeker_dashboard.html')

# Employer Dashboard
def employer_dashboard():
    return render_template('employer_dashboard.html')

