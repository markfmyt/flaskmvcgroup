from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application

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
        return jsonify({"message": "Job seeker not found."}), 404

    success, application = job_seeker.apply_to_job(job_id, application_text)  # Attempt to apply for the job

    if success:
        return jsonify({"application_id": application.application_id, "message": "Application submitted successfully."}), 201  # Return application ID and success message
    else:
        return jsonify({"message": application}), 400  # Return the error message if the application fails

# View All Applications by Job Seeker
@job_seeker_views.route('/api/jobs/applications', methods=['GET'])
@jwt_required()
def view_job_status_all_api():
    job_seeker_id = get_jwt_identity()  # Get the job seeker ID from the JWT

    job_seeker = JobSeeker.query.get(job_seeker_id)  # Fetch the JobSeeker instance
    if not job_seeker:
        return jsonify({"message": "Job seeker not found."}), 404

    success, application_list = job_seeker.view_job_status_all()  

    if success:
        return jsonify(application_list), 200  # Return the application list with a success status
    else:
        return jsonify({"message": application_list}), 404  # Return the message if no applications found


@job_seeker_views.route('/api/jobs/status/<int:application_id>', methods=['GET'])
@jwt_required()
def view_application_status_api(application_id):
    job_seeker_id = get_jwt_identity()  # Get the job seeker ID from the JWT

    job_seeker = JobSeeker.query.get(job_seeker_id)  # Fetch the JobSeeker instance
    if not job_seeker:
        return jsonify({"message": "Job seeker not found."}), 404

    success, application_details = job_seeker.view_job_status(application_id)  # Attempt to view the application status

    if success:
        return jsonify(application_details), 200  # Return application details with a 200 status code
    else:
        return jsonify({"message": application_details}), 404  # Return the error message if the application is not found
