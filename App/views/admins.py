from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# Admin Commands
@admin_views.route('/api/admin/print_all', methods=['GET'])
@jwt_required()
def print_all_entities_api():
    admin_id = get_jwt_identity()
    return get_all_entities(admin_id)

@admin_views.route('/api/admin/drop_all', methods=['DELETE'])
@jwt_required()
def drop_all_api():
    admin_id = get_jwt_identity()
    return drop_database(admin_id)

@admin_views.route('/api/admin/remove_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user_api(user_id):
    admin_id = get_jwt_identity()
    return remove_user(admin_id,user_id)

@admin_views.route('/api/admin/remove_job/<int:job_id>', methods=['DELETE'])
@jwt_required()
def remove_job_api(job_id):
    admin_id = get_jwt_identity()
    return remove_job(admin_id,job_id)

@admin_views.route('/api/admin/remove_application/<int:application_id>', methods=['DELETE'])
@jwt_required()
def remove_application_api(application_id):
    admin_id = get_jwt_identity()
    return remove_application(admin_id, application_id)

# Get All Users
@admin_views.route('/api/users', methods=['GET'])
@jwt_required()
def list_users_api():
    admin_id = get_jwt_identity()
    return get_all_users(admin_id)