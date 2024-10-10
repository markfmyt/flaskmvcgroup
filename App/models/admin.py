from App.database import db
from .user import User
from .job import Job
from .application import Application

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username, password, email):
        super().__init__(username, password, email, user_type='admin')  # Call the parent class constructor

    # def drop_database(self):
    #     # Check if the admin exists
    #     if not self:
    #         return (False, "Admin not found.")  # Admin not found

    #     db.drop_all()
    #     return (True, "Database dropped successfully.")  # Indicate that the database has been dropped

    # def remove_user(self, user_id):
    #     # Prevent admin from deleting themselves
    #     if self.id == user_id:
    #         return (False, "An admin cannot delete themselves.")  # An admin cannot delete themselves

    #     user = User.query.get(user_id)
    #     if not user:
    #         return (False, "User not found.")  # User not found

    #     # Prevent admins from deleting other admins
    #     if user.user_type == 'admin':
    #         return (False, "Admins cannot delete other admins.")  # Admins cannot delete other admins

    #     # Proceed with user deletion
    #     db.session.delete(user)
    #     db.session.commit()
    #     return (True, "User removed successfully.")  # Indicate that the user has been removed

    # def remove_job(self, job_id):
    #     job = Job.query.get(job_id)
    #     if not job:
    #         return (False, "Job not found.")  # Job not found

    #     # Proceed with job deletion
    #     db.session.delete(job)
    #     db.session.commit()
    #     return (True, "Job removed successfully.")  # Indicate that the job has been removed

    # def remove_application(self, application_id):
    #     application = Application.query.get(application_id)
    #     if not application:
    #         return (False, "Application not found.")  # Application not found

    #     db.session.delete(application)
    #     db.session.commit()
    #     return (True, "Application removed successfully.")  # Indicate that the application has been removed
