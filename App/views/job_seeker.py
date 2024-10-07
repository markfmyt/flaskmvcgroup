from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *

job_seeker_views = Blueprint('job_seeker_views', __name__, template_folder='../templates')




# Apply for Job
@job_seeker_views.route('/api/jobs/apply', methods=['POST'])
@jwt_required()
def apply_job_api():
    data = request.json
    job_id = data.get('job_id')
    job_seeker_id = get_jwt_identity()
    application_text = data.get('application_text')
    return apply_to_job(job_id, job_seeker_id, application_text)

# View All Applications by Job Seeker
@job_seeker_views.route('/api/jobs/applications', methods=['GET'])
@jwt_required()
def view_job_status_all_api():
    job_seeker_id = get_jwt_identity()
    applications = view_job_status_all(job_seeker_id)

    # Check if the request is asking for JSON (e.g., from Postman)
    if request.accept_mimetypes['application/json']:
        return applications  # Return JSON for Postman or API consumers
    
    # Otherwise, render the HTML for browsers
    # return render_template('applications.html', applications=applications)


@job_seeker_views.route('/api/jobs/status/<int:application_id>', methods=['GET'])
@jwt_required()
def view_application_status_api(application_id):
    job_seeker_id = get_jwt_identity()
    return view_job_status(job_seeker_id, application_id)