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

@pytest.fixture(scope="module")
def init_database():

    create_user("seeker2", "seekerpass", "seeker2@mail.com", "job_seeker")
    create_user("employer2", "employerpass", "employer2@mail.com", "employer")
    create_job(2, "Data Analyst", "Analyze data using Python and SQL")
    
    # Used for job status all
    create_job(2, "Analyst of Data", "Analyze data using SQL")
    apply_to_job(2, 1, "I have experience in data analysis with Python and SQL")

    db.session.commit()

class TestJobSeeker:
    def test_apply_to_job(self,init_database):
        application_result = apply_to_job(1, 1, "I have experience in data analysis with Python and SQL")
        assert application_result is True
    
    def test_apply_to_job_fail(self,init_database):
        application_result = apply_to_job(999, 1, "I have experience in data analysis with Python") # Invalid job
        assert application_result is None

    def test_view_job_status_all(self,init_database):
        # View all job application statuses for the job seeker
        application = view_job_status_all(1)  # Job seeker ID 1
        assert application is not None

    def test_view_job_status_all_fail(self,init_database):
        application = view_job_status_all(999)  # Invalid Job Seeker ID
        assert application is None

    def test_view_job_status(self,init_database):
        # View status of a specific job application
        application_status = view_job_status(1, 1)
        assert application_status is not None
    
    def test_view_job_status_fail(self,init_database):
        application_status = view_job_status(1, 999)
        assert application_status is None

    def test_get_all_jobs(self,init_database):
  
        jobs = get_all_jobs()
        assert jobs is not None

