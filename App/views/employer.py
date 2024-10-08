from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application

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
    success, message = employer.review_application(application_id, decision.lower() == 'accept')
    
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400


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
    success, job = employer.create_job(category, description)

    if success:
        return jsonify({
            "message": "Job created successfully.",
            "job": {
                "job_id": job.id,
                "category": job.category,
                "description": job.description,
                "employer_id": job.employer_id
            }
        }), 201
    else:
        return jsonify({"error": job}), 400


@employer_views.route('/api/employer/view_applicants/<int:job_id>', methods=['GET'])
@jwt_required()
def get_applicants_for_job_api(job_id):
    employer_id = get_jwt_identity()  # Get the current employer's ID from the JWT
    employer = Employer.query.get(employer_id)  # Fetch the employer instance

    if not employer:
        return jsonify({"error": f"Employer ID {employer_id} not found."}), 404

    # Use the method from the Employer class to get applicants for the specified job
    success, result = employer.get_applicants_for_job(job_id)

    if success:
        return jsonify({
            "applicants": result
        }), 200 
    else:
        return jsonify({"error": result}), 400