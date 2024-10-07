from App.models import User
from App.database import db

# def create_user(username, password):
#     newuser = User(username=username, password=password)
#     db.session.add(newuser)
#     db.session.commit()
#     return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users(admin_id):
    # Check if the admin_id is valid
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':  # Ensure the user is an admin
        return jsonify({"error": "Unauthorized: Only admins can view all users."}), 403

    users = User.query.all()
    return jsonify(users), 200  # Return users with a 200 OK status code

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    