import pytest
from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_user,
    create_job,
    apply_to_job,
    view_job_status_all,
    view_job_status,
    get_all_jobs,
)

@pytest.fixture(autouse=True, scope="module")
def test_client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
        db.create_all()
        yield app.test_client()
        db.drop_all()

class TestJobSeeker:
    def test_apply_to_job(self):
        # Create a job seeker
        seeker_created = create_user("seeker2", "seekerpass", "seeker2@mail.com", "job_seeker")
        assert seeker_created is True

        # Create a job to apply to
        employer_created = create_user("employer2", "employerpass", "employer2@mail.com", "employer")
        assert employer_created is True
        job_created = create_job(2, "Data Analyst", "Analyze data using Python and SQL")
        assert job_created is True

        # Apply to the job
        application_result = apply_to_job(1, 1, "I have experience in data analysis with Python and SQL")
        assert application_result is True

    def test_view_job_status_all(self):
        # View all job application statuses for the job seeker
        application = view_job_status_all(1)  # Job seeker ID 1
        assert application is not None
        assert len(application) > 0

    def test_view_job_status(self):
        # View status of a specific job application
        application_status = view_job_status(1, 1)  # Job seeker ID 5, Application ID 2
        assert application_status is not None
        assert hasattr(application_status, 'is_accepted')

    def test_get_all_jobs(self):
            
        jobs = get_all_jobs()
        assert jobs is not None
        assert len(jobs) > 0
        assert any(job.category == "Data Analyst" for job in jobs)