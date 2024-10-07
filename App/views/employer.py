from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import *


employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

# Employer Commands
@employer_views.route('/api/employer/review/<int:application_id>', methods=['POST'])
@jwt_required()
def review_application_api(application_id):
    employer_id = get_jwt_identity()
    data = request.json
    decision = data.get('decision')
    return review_application(employer_id, application_id, decision.lower() == 'accept') # This acts as a boolean value

@employer_views.route('/api/employer/create_job', methods=['POST'])
@jwt_required()
def create_job_api():
    data = request.json
    category = data.get('category')
    description = data.get('description')
    employer_id = get_jwt_identity()
    return create_job(category, description, employer_id)

@employer_views.route('/api/employer/view_applicants/<int:job_id>', methods=['GET'])
@jwt_required()
def get_applicants_for_job_api(job_id):
    employer_id = get_jwt_identity()
    return get_applicants_for_job(employer_id, job_id)