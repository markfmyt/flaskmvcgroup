from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import db, User, Admin, Employer, JobSeeker, Job, Application

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# Admin Commands
@admin_views.route('/api/admin/print_all', methods=['GET'])
@jwt_required()
def print_all_entities_api():
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, entities = admin.get_all_entities()  # Call the method to get all users and jobs

    if not success:
        return jsonify({"message": entities}), 400  # Return error if not successful

    return jsonify({"data": entities}), 200  # Return data

@admin_views.route('/api/admin/drop_all', methods=['DELETE'])
@jwt_required()
def drop_all_api():
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, message = admin.drop_database()  # Call the method to drop the database

    if not success:
        return jsonify({"message": message}), 400  # Return error if not successful

    return jsonify({"message": message}), 200  # Return success message


@admin_views.route('/api/admin/remove_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user_api(user_id):
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, message = admin.remove_user(user_id)  # Call the method to remove the user

    if not success:
        return jsonify({"message": message}), 404  # Return error if not successful

    return jsonify({"message": message}), 200  # Return success message


@admin_views.route('/api/admin/remove_job/<int:job_id>', methods=['DELETE'])
@jwt_required()
def remove_job_api(job_id):
    admin_id = get_jwt_identity() 
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, message = admin.remove_job(job_id)  # Call the method to remove the job

    if not success:
        return jsonify({"message": message}), 404  # Return error if not successful

    return jsonify({"message": message}), 200  # Return success message


@admin_views.route('/api/admin/remove_application/<int:application_id>', methods=['DELETE'])
@jwt_required()
def remove_application_api(application_id):
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, message = admin.remove_application(application_id)  # Call the method to remove the application

    if not success:
        return jsonify({"message": message}), 404  # Return error if not successful

    return jsonify({"message": message}), 200  # Return success message


# Get All Users
@admin_views.route('/api/users', methods=['GET'])
@jwt_required()
def list_users_api():
    admin_id = get_jwt_identity()  # Get the current admin's ID from the JWT
    admin = Admin.query.get(admin_id)  # Fetch the admin instance

    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    success, data = admin.get_all_entities()  # Call the method to get users and jobs
    if not success:
        return jsonify({"message": data}), 404  # Return error if not successful

    # Format the user data as needed
    formatted_users = [{"id": user.id, "username": user.username, "email": user.email} for user in data["users"]]

    return jsonify({
        "users": formatted_users
    }), 200
