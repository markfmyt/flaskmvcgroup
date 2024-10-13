from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def create_job(employer_id,category, description):
    employer = Employer.query.get(employer_id)
    if not employer:
        return None 
    
    job = Job(employer_id = employer_id,category=category, description=description)
    db.session.add(job)
    try:
        db.session.commit() 
        return True 
    except Exception as e:
        db.session.rollback() 
        return None  

def get_applicants_for_job(job_id):
    applicant_list = Application.query.filter_by(job_id=job_id).all()
    if applicant_list:
        return applicant_list
    return None

def review_application(application_id, is_accepted):
    application = Application.query.get(application_id)
    if application:
        application.is_accepted = is_accepted
        try:
            db.session.commit()  
            return True 
        except Exception as e:
            db.session.rollback() 
            return None 
    return None 
