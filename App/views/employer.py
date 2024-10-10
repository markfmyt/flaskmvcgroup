from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from App.controllers import employer

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

# Employer Commands
@employer_views.route('/api/employer/review/<int:application_id>', methods=['POST'])
@jwt_required()
def review_application_api(application_id):
    employer_id = get_jwt_identity()  # Get the current employer's ID from the JWT
    employer = Employer.query.get(employer_id)  # Fetch the employer instance

    if not employer:
        return jsonify({"error": f"Employer ID {employer_id} not found."}), 404
    
    data = request.json  # Get the JSON data from the request
    decision = data.get('decision')  # Expecting 'accept' or 'reject'

    if decision not in ['accept', 'reject']:
        return jsonify({"error": "Invalid decision. Must be 'accept' or 'reject'."}), 400

    # Call the review_application method with the appropriate boolean value
    message = review_application(application_id, decision.lower() == 'accept')
    
    if message and decision.lower() == 'accept':
        return jsonify({"message": "Application has been accepted"}), 200
    elif message and decision.lower() != 'accept':
        return jsonify({"message": "Application has been accepted"}), 200

    return jsonify({"error": "Something went wrong, application not reviewed"}), 400



@employer_views.route('/api/employer/create_job', methods=['POST'])
@jwt_required()
def create_job_api():
    employer_id = get_jwt_identity()  # Get the current employer's ID from the JWT
    employer = Employer.query.get(employer_id)  # Fetch the employer instance

    if not employer:
        return jsonify({"error": f"Employer ID {employer_id} not found."}), 404

    data = request.json
    category = data.get('category')
    description = data.get('description')

    # Validate input
    if not category or not description:
        return jsonify({"error": "Category and description are required."}), 400

    # Create the job using the method from the Employer class
    job = create_job(employer_id,category, description)

    if job:
        return jsonify({"message": "Job created successfully.",}), 201
    else:
        return jsonify({"error": "Job not created, something went wrong!"}), 400


@employer_views.route('/api/employer/view_applicants/<int:job_id>', methods=['GET'])
@jwt_required()
def get_applicants_for_job_api(job_id):
    employer_id = get_jwt_identity()  # Get the current employer's ID from the JWT
    employer = Employer.query.get(employer_id)  # Fetch the employer instance

    if not employer:
        return jsonify({"error": f"Employer ID {employer_id} not found."}), 404

    result = get_applicants_for_job(job_id)  # Get applicants for the specified job

    if result is None:
        return jsonify({"error": "No applicants found."}), 404  # Use 404 for not found

    applicants_data = [
        {
            'application_id': application.application_id,
            'job_id': application.job_id,
            'job_seeker_id': application.job_seeker_id,
            'application_text': application.application_text,
            'is_accepted': application.is_accepted,
        }
        for application in result
    ]
    
    return jsonify({"applicants": applicants_data}), 200