from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from App.controllers import job_seeker

job_seeker_views = Blueprint('job_seeker_views', __name__, template_folder='../templates')

# Apply for Job
@job_seeker_views.route('/api/jobs/apply', methods=['POST'])
@jwt_required()
def apply_job_api():
    data = request.json
    job_id = data.get('job_id')
    job_seeker_id = get_jwt_identity()  # Get the job seeker ID from the JWT
    application_text = data.get('application_text')

    job_seeker = JobSeeker.query.get(job_seeker_id)  # Fetch the JobSeeker instance
    if not job_seeker:
        return jsonify({"error": "Job seeker not found."}), 404
    
    existing_application = Application.query.filter_by(job_id=job_id, job_seeker_id=job_seeker_id).first()
    if existing_application:
        return jsonify({"error": "You have already applied for this job."}), 400

    application = apply_to_job(job_id, job_seeker_id, application_text)  # Attempt to apply for the job

    if application:
        return jsonify({"message": "Application submitted successfully."}), 201  # Return application ID and success message
    else:
        return jsonify({"error": "Something went wrong! Application not made"}), 400  # Return the error message if the application fails

# View All Applications by Job Seeker
@job_seeker_views.route('/api/jobs/applications', methods=['GET'])
@jwt_required()
def view_job_status_all_api():
    job_seeker_id = get_jwt_identity()  # Get the job seeker ID from the JWT

    job_seeker = JobSeeker.query.get(job_seeker_id)  # Fetch the JobSeeker instance
    if not job_seeker:
        return jsonify({"error": "Job seeker not found."}), 404

    application_list = view_job_status_all(job_seeker_id)  

    if application_list is None:
        return jsonify({"error": "No applications found."}), 404  # Return error if no applications found

    applications_data = [
        {
            'application_id': application.application_id,
            'job_id': application.job_id,
            'job_seeker_id': application.job_seeker_id,
            'application_text': application.application_text,
            'is_accepted': application.is_accepted,
        }
        for application in application_list
    ]
    
    return jsonify(applications_data), 200

@job_seeker_views.route('/api/jobs/status/<int:application_id>', methods=['GET'])
@jwt_required()
def view_application_status_api(application_id):
    job_seeker_id = get_jwt_identity()  # Get the job seeker ID from the JWT

    job_seeker = JobSeeker.query.get(job_seeker_id)  # Fetch the JobSeeker instance
    if not job_seeker:
        return jsonify({"error": "Job seeker not found."}), 404

    application_details = view_job_status(job_seeker_id, application_id)  # Attempt to view the application status

    if application_details is None:
        return jsonify({"error": "No such application!"}), 404  # Return the error message if the application is not found

    application_data = {
        'application_id': application_details.application_id,
        'job_id': application_details.job_id,
        'job_seeker_id': application_details.job_seeker_id,
        'application_text': application_details.application_text,
        'is_accepted': application_details.is_accepted,
    }
    
    return jsonify(application_data), 200