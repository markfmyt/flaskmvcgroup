import click
from flask import Flask, jsonify, request
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from App.database import db, init_db, get_migrate
from App.models import User, Admin, Employer, JobSeeker, Job, Application
from App.controllers import (
    create_user, login_user, review_application,
    view_job_status_all, view_job_status, create_job,
    apply_to_job, get_all_jobs, get_all_users,
    drop_database, remove_application, remove_job, remove_user,
    initialize, get_all_entities, get_applicants_for_job
)
from App.main import create_app

app = create_app()
migrate = get_migrate(app)
jwt = JWTManager(app)
app.debug = True

# CLI command to initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init_db_command():
    initialize()
    print('Database initialized.')

# User Registration
@app.route('/api/users/signup', methods=['POST'])
def signup_user_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    return create_user(username, password, email, role)

# User Login
@app.route('/api/users/login', methods=['POST'])
def login_user_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    return login_user(username, password)

# Get All Users
@app.route('/api/users', methods=['GET'])
@jwt_required()
def list_users_api():
    return jsonify(get_all_users()), 200

# Job Postings
@app.route('/api/jobs', methods=['GET'])
def list_jobs_api():
    return jsonify(get_all_jobs()), 200

# Apply for Job
@app.route('/api/jobs/apply', methods=['POST'])
@jwt_required()
def apply_job_api():
    data = request.json
    job_id = data.get('job_id')
    job_seeker_id = get_jwt_identity()
    application_text = data.get('application_text')
    return apply_to_job(job_id, job_seeker_id, application_text)

# View All Applications by Job Seeker
@app.route('/api/jobs/applications', methods=['GET'])
@jwt_required()
def view_job_status_all_api():
    job_seeker_id = get_jwt_identity()
    return view_job_status_all(job_seeker_id)

# View Application Status
@app.route('/api/jobs/status/<int:application_id>', methods=['GET'])
@jwt_required()
def view_application_status_api(application_id):
    job_seeker_id = get_jwt_identity()
    return view_job_status(job_seeker_id, application_id)

# Employer Commands
@app.route('/api/employer/review/<int:application_id>', methods=['POST'])
@jwt_required()
def review_application_api(application_id):
    employer_id = get_jwt_identity()
    data = request.json
    decision = data.get('decision')
    return review_application(employer_id, application_id, decision.lower() == 'accept') # This acts as a boolean value

@app.route('/api/employer/create_job', methods=['POST'])
@jwt_required()
def create_job_api():
    data = request.json
    category = data.get('category')
    description = data.get('description')
    employer_id = get_jwt_identity()
    return create_job(category, description, employer_id)

@app.route('/api/employer/view_applicants/<int:job_id>', methods=['GET'])
@jwt_required()
def get_applicants_for_job_api(job_id):
    employer_id = get_jwt_identity()
    return get_applicants_for_job(employer_id, job_id)

# Admin Commands
@app.route('/api/admin/print_all', methods=['GET'])
@jwt_required()
def print_all_entities_api():
    admin_id = get_jwt_identity()
    return get_all_entities(admin_id)

@app.route('/api/admin/drop_all', methods=['DELETE'])
@jwt_required()
def drop_all_api():
    admin_id = get_jwt_identity()
    return drop_database(admin_id)

@app.route('/api/admin/remove_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user_api(user_id):
    admin_id = get_jwt_identity()
    return remove_user(admin_id,user_id)

@app.route('/api/admin/remove_job/<int:job_id>', methods=['DELETE'])
@jwt_required()
def remove_job_api(job_id):
    admin_id = get_jwt_identity()
    return remove_job(admin_id,job_id)

@app.route('/api/admin/remove_application/<int:application_id>', methods=['DELETE'])
@jwt_required()
def remove_application_api(application_id):
    admin_id = get_jwt_identity()
    return remove_application(admin_id, application_id)

if __name__ == "__main__":
    app.run(port=5000)