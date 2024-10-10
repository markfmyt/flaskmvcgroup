from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from App.controllers import admin
from App.controllers.user import get_all_users
from App.controllers.admin import *
admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/api/admin/remove_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user_api(user_id):
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    if admin_id == user_id:
        return "An admin cannot delete themselves."
        
    message = remove_user(user_id)  # Call the method to remove the user

    if not message:
        return jsonify({"error": f'User with id: {user_id} not removed'}), 404  # Return error if not successful

    return jsonify({"message": f'User with id: {user_id} removed'}), 200  # Return success message


@admin_views.route('/api/admin/remove_job/<int:job_id>', methods=['DELETE'])
@jwt_required()
def remove_job_api(job_id):
    admin_id = get_jwt_identity() 
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    message = remove_job(job_id)  # Call the method to remove the job
    print(message)
    
    if message is None:
        jsonify({"error": f'Job with id: {job_id} not removed'}), 404  # Return error if not successful

    return jsonify({"message": f'Job with id: {job_id} removed'}), 200  # Return success message


@admin_views.route('/api/admin/remove_application/<int:application_id>', methods=['DELETE'])
@jwt_required()
def remove_application_api(application_id):
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    message = remove_application(application_id)  # Call the method to remove the application

    if not message:
        return jsonify({"error": f'Application with id: {application_id} not removed'}), 404  # Return error if not successful

    return jsonify({"message": f'Application with id: {application_id} removed'}), 200  # Return success message


# Get All Users
@admin_views.route('/api/users', methods=['GET'])
@jwt_required()
def list_users_api():
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    data = get_all_users()  # Call the method to get users
    if not data:  # data is a list now, check if it's empty
        return jsonify({"message": "No users found."}), 404  # Return error if not successful

    # Format the user data as needed
    formatted_users = [{"id": user["id"], "username": user["username"], "email": user["email"]} for user in data]

    return jsonify({
        "users": formatted_users
    }), 200
