from flask import Blueprint, render_template, jsonify, request
from App.controllers import *
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