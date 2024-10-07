from App.database import db
from .user import User
from .job import Job
from .application import Application

class JobSeeker(User):
    __tablename__ = 'job_seekers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Set in such a way that if a JobSeeker gets deleted, their applications get deleted as well
    applications = db.relationship('Application', backref='job_seeker', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'job_seeker',
    }

    def __init__(self, username, password, email):
        super().__init__(username, password, email, user_type='job_seeker')  # Call the parent class constructor

    def apply_to_job(self, job_id, application_text):
        job = Job.query.get(job_id)
        if not job:
            return (False, "Job not found.")  # Job not found

        # Check if the job seeker has already applied for this job
        existing_application = Application.query.filter_by(job_id=job_id, job_seeker_id=self.id).first()
        if existing_application:
            return (False, "Already applied for this job.")  # Already applied

        # Create a new application
        application = Application(job_id=job_id, job_seeker_id=self.id, application_text=application_text)
        db.session.add(application)
        db.session.commit()
        
        return (True, application)  # Return success and the created application object

    def view_job_status_all(self):
        applications = Application.query.filter_by(job_seeker_id=self.id).all()
        if not applications:
            return (False, "No applications found.")  # No applications found

        application_list = []
        for application in applications:
            application_list.append({
                "job_id": application.job_id,
                "job_category": application.job.category,
                "description": application.job.description,
                "status": 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
            })
        return (True, application_list)  # Return success and the list of applications

    def view_job_status(self, application_id):
        application = Application.query.filter_by(job_seeker_id=self.id, application_id=application_id).first()
        if not application:
            return (False, "No application found.")  # No application found

        status = 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
        return (True, {
            "job_id": application.job_id,
            "job_category": application.job.category,
            "description": application.job.description,
            "status": status
        })  # Return success and the application details
