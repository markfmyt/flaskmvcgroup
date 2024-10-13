from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def get_all_jobs():
    jobs = Job.query.all()
    if jobs:
        return jobs
    return None

def apply_to_job(job_id, job_seeker_id, application_text):

    job = Job.query.get(job_id)
    if not job:
        return None  # Job doesn't exist, so application can't be made

    job_seeker = JobSeeker.query.get(job_seeker_id)
    if not job_seeker:
        return None  # Job seeker doesn't exist, so application can't be made

    application = Application(job_id=job_id, job_seeker_id=job_seeker_id, application_text=application_text)
    db.session.add(application)
    try:
        db.session.commit()
        return True 
    except Exception as e:
        db.session.rollback()
        return None
 

def view_job_status_all(job_seeker_id):
    application_list = Application.query.filter_by(job_seeker_id=job_seeker_id).all()
    if application_list:
        return application_list
    return None

def view_job_status(job_seeker_id, application_id):
    application = Application.query.filter_by(job_seeker_id=job_seeker_id, application_id=application_id).first()
    if application:
        return application
    return None
