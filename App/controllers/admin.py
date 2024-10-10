from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def get_all_entities():
    users = get_all_users()
    jobs = get_all_jobs()

    return {
        "users": users,
        "jobs": jobs
    }

def drop_database():
    return db.drop_all()

def remove_user(user_id):
    user = User.query.get(user_id)
    if user: 
        db.session.delete(user)
        try:
            db.session.commit() 
            return True  
        except Exception as e:
            db.session.rollback()  
            return None  
    return None  

def remove_job(job_id):
    job = Job.query.get(job_id)
    if job: 
        db.session.delete(job)
        try:
            db.session.commit() 
            return True  
        except Exception as e:
            db.session.rollback()
            return None  
    return None  

def remove_application(application_id):
    application = Application.query.get(application_id)
    if application:  
        db.session.delete(application)
        try:
            db.session.commit()  
            return True  
        except Exception as e:
            db.session.rollback()
            return None  
    return None  
