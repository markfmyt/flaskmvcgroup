from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify



# Controller function to initialize the database
def initialize():
    db.drop_all()
    db.create_all()
    
    return jsonify({"message": "Database initialized."}), 200

'''
User Controllers
'''

def create_user(username, password, email, role):
    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return jsonify({"error": f"Username '{username}' is already taken."}), 400
    
    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return jsonify({"error": f"Email '{email}' is already registered."}), 400

    if role not in ['admin', 'employer', 'job_seeker']:
        return jsonify({"error": f"Invalid role '{role}'."}), 400

    hashed_password = generate_password_hash(password)
    user = None

    if role == 'employer':
        user = Employer(username=username, password=hashed_password, email=email, company_name="DefaultCompany")
    elif role == 'job_seeker':
        user = JobSeeker(username=username, password=hashed_password, email=email)
    elif role == 'admin':
        user = Admin(username=username, password=hashed_password, email=email)

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User '{username}' created successfully!"}), 201

def login_user(username, password):

    print(f"Login attempt for user: {username}")
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print("User not found")
        return jsonify({"error": "User not found."}), 404
    
    print(f"Found user: {user.username}, Hashed Password: {user.password}")
    
    if check_password_hash(user.password, password):
        print("Password matched!")
        access_token = create_access_token(identity=user.id)
        print(f"Generated access token: {access_token}")
        return jsonify(access_token=access_token), 200
    
    print("Password did not match")
    return jsonify({"error": "Invalid username or password."}), 401


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

'''
Job Controllers
'''

def get_all_jobs():
    jobs = Job.query.all()
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            "id": job.id,
            "category": job.category,
            "description": job.description,
            "employer_id": job.employer_id
        })
    return jobs_list

def apply_to_job(job_id, job_seeker_id, application_text):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": f"Job ID {job_id} not found."}), 404

    job_seeker = JobSeeker.query.get(job_seeker_id)
    if not job_seeker:
        return jsonify({"error": f"Job Seeker ID {job_seeker_id} not found."}), 404

    application = Application(job_id=job_id, job_seeker_id=job_seeker_id, text=application_text)
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": f"Job Seeker {job_seeker_id} applied to Job {job_id}."}), 201

def view_job_status_all(job_seeker_id):
    applications = Application.query.filter_by(job_seeker_id=job_seeker_id).all()
    if not applications:
        return jsonify({"error": f"No applications found for Job Seeker {job_seeker_id}."}), 404

    application_list = []
    for application in applications:
        application_list.append({
            "job_id": application.job_id,
            "job_category": application.job.category,
            "description": application.job.description,
            "status": 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
        })
    return jsonify(application_list), 200

def view_job_status(job_seeker_id, application_id):
    application = Application.query.filter_by(job_seeker_id=job_seeker_id, application_id=application_id).first()
    if not application:
        return jsonify({"error": f"No application found for Job Seeker {job_seeker_id} with Application ID {application_id}."}), 404

    status = 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
    return jsonify({
        "job_id": application.job_id,
        "job_category": application.job.category,
        "description": application.job.description,
        "status": status
    }), 200

'''
Employer Controllers
'''

def create_job(category, description, employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({"error": f"Employer ID {employer_id} not found."}), 404

    job = Job(category=category, description=description, employer_id=employer_id)
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": f"Job created with category '{category}' by Employer {employer_id}."}), 201

def get_applicants_for_job(employer_id, job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": f"Job ID {job_id} not found."}), 404
    
    # Check if the employer owns the job
    if job.employer_id != employer_id:
        return jsonify({"error": "You are not authorized to view the applicants for this job."}), 403

    applications = Application.query.filter_by(job_id=job_id).all()
    if not applications:
        return jsonify({"error": f"No applications found for Job ID {job_id}."}), 404

    applicant_list = []
    for application in applications:
        applicant_list.append({
            "application_id": application.id,
            "job_seeker_id": application.job_seeker_id,
            "status": 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
        })
    return applicant_list


def review_application(employer_id, application_id, is_accepted):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({"error": f"Application ID {application_id} not found."}), 404
    
    job = Job.query.get(application.job_id)  # Get the job associated with the application
    if not job or job.employer_id != employer_id:
        return jsonify({"error": "You are not authorized to review this application."}), 403
    
    application.is_accepted = is_accepted
    db.session.commit()
    
    status = 'accepted' if is_accepted else 'rejected'
    return jsonify({"message": f'Application {application_id} has been {status}.'}), 200

'''
Admin Controllers
'''

def get_all_entities(admin_id):
    # Check if admin exists in the database
    admin = User.query.filter_by(id=admin_id, role='admin').first()
    if not admin:
        return jsonify({"error": f"Admin with ID {admin_id} not found."}), 404

    users = get_all_users()
    jobs = get_all_jobs()
    
    return jsonify({
        "users": users,
        "jobs": jobs
    }), 200

def drop_database(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"error": f"Admin ID {admin_id} not found."}), 404

    db.drop_all()
    return jsonify({"message": "Database dropped."}), 200

def remove_user(admin_id, user_id):
    # Check if the admin exists
    admin = User.query.filter_by(id=admin_id, role='admin').first()
    if not admin:
        return jsonify({"error": f"Admin with ID {admin_id} not found."}), 404

    # Prevent admin from deleting themselves
    if admin_id == user_id:
        return jsonify({"error": "An admin cannot delete themselves."}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": f"User ID {user_id} not found."}), 404

    # Prevent admins from deleting other admins
    if user.role == 'admin':
        return jsonify({"error": "Admins cannot delete other admins."}), 403

    # Proceed with user deletion
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} removed successfully."}), 200

def remove_job(admin_id, job_id):
    # Check if the admin exists
    admin = User.query.filter_by(id=admin_id, role='admin').first()
    if not admin:
        return jsonify({"error": f"Admin with ID {admin_id} not found."}), 404

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": f"Job ID {job_id} not found."}), 404

    # Proceed with job deletion
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": f"Job {job_id} removed successfully."}), 200


def remove_application(admin_id, application_id):
    # Check if the admin_id is valid
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':  # Ensure the user is an admin
        return jsonify({"error": "Unauthorized: Only admins can remove applications."}), 403

    application = Application.query.get(application_id)
    if not application:
        return jsonify({"error": f"Application ID {application_id} not found."}), 404

    db.session.delete(application)
    db.session.commit()
    return jsonify({"message": f"Application {application_id} removed successfully."}), 200
