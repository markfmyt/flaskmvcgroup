import pytest
from App.main import create_app
from App.database import db, create_db
from App.models import Employer, JobSeeker, Job, Application
from App.controllers import get_all_jobs, apply_to_job, view_job_status_all, view_job_status

@pytest.fixture(autouse=True)
def test_client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        create_db()  # Create the database schema
        db.create_all()

        # Setup test data
        employer = Employer(username="employer1", password="employerpass", email="employer1@mail.com")
        job_seeker = JobSeeker(username="job_seeker1", password="seekerpass", email="seeker1@mail.com")
        job = Job(category="Software Development", description="Develop software applications.", employer_id=1)

        db.session.add(employer)
        db.session.add(job_seeker)
        db.session.add(job)
        db.session.commit()

        yield  # Test function will run here

        db.session.remove()
        db.drop_all()  # Cleanup after tests

def test_get_all_jobs(test_client):
    jobs = get_all_jobs()
    assert jobs is not None
    assert len(jobs) == 1
    assert jobs[0].category == "Software Development"

def test_apply_to_job(test_client):
    result = apply_to_job(job_id=1, job_seeker_id=1, application_text="I am interested in this position.")
    assert result is True  # Check if the application was successful

    # Check if the application was added to the database
    application = Application.query.filter_by(job_id=1, job_seeker_id=1).first()
    assert application is not None
    assert application.application_text == "I am interested in this position."

def test_view_job_status_all(test_client):
    apply_to_job(job_id=1, job_seeker_id=1, application_text="First application.")
    apply_to_job(job_id=1, job_seeker_id=1, application_text="Second application.")

    applications = view_job_status_all(job_seeker_id=1)
    assert applications is not None
    assert len(applications) == 2  # We applied twice

def test_view_job_status(test_client):
    apply_to_job(job_id=1, job_seeker_id=1, application_text="One more application.")

    app_status = view_job_status(job_seeker_id=1, application_id=1)
    assert app_status is not None
    assert app_status.application_text == "I am interested in this position."  # Check the first application

    # Check for an application that doesn't exist
    non_existing_status = view_job_status(job_seeker_id=1, application_id=999)
    assert non_existing_status is None  # Application with ID 999 should not exist
