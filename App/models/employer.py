from App.database import db
from .job import Job
from .job_seeker import JobSeeker
from .user import User
from .application import Application

class Employer(User):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)

    # Set in such a way that if an Employer gets deleted, their job_listings gets deleted as well
    job_listings = db.relationship('Job', backref='employer', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, email, company_name):
        super().__init__(username, password, email, user_type='employer')  # Call the parent class constructor
        self.company_name = company_name
    
    # def create_job(self, category, description):
    #     job = Job(category=category, description=description, employer_id=self.id)
    #     db.session.add(job)
    #     db.session.commit()
    #     return (True, job)  # Return success and the created job object

    # def get_applicants_for_job(self, job_id):
    #     job = Job.query.get(job_id)
    #     if not job:
    #         return (False, "Job not found.")  # Job not found

    #     # Check if the employer owns the job
    #     if job.employer_id != self.id:
    #         return (False, "Not authorized to view applicants.")  # Not authorized to view applicants

    #     applications = Application.query.filter_by(job_id=job_id).all()
    #     if not applications:
    #         return (False, "No applications found.")  # No applications found

    #     applicant_list = []
    #     for application in applications:
    #         applicant_list.append({
    #             "application_id": application.application_id,
    #             "job_seeker_id": application.job_seeker_id,
    #             "status": 'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'
    #         })
    #     return (True, applicant_list)  # Return success and the list of applicants

    # def review_application(self, application_id, is_accepted):
    #     application = Application.query.get(application_id)
    #     if not application:
    #         return (False, "Application not found.")  # Application not found

    #     job = Job.query.get(application.job_id)  # Get the job associated with the application
    #     if not job or job.employer_id != self.id:
    #         return (False, "Not authorized to review the application.")  # Not authorized to review the application

    #     application.is_accepted = is_accepted
    #     db.session.commit()
        
    #     if application.is_accepted is True:
    #         return (True, f'Application {application_id} has been accepted.')
    #     elif application.is_accepted is False:
    #         return (False, f'Application {application_id} has been rejected.')
    #     else:
    #         return (False, f'Application {application_id} status is undetermined/pending.')

                                        
