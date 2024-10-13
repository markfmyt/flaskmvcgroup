import pytest
from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_user,
    create_job,
    get_applicants_for_job,
    review_application,
    apply_to_job
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
    # Create some initial seed data
    create_user("employer1", "employerpass", "employer1@mail.com", "employer")
    create_user("seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
    create_job(1, "Backend", "Develop backend software applications.")
    apply_to_job(1, 2, "I am interested in this position.")
    db.session.commit()

class TestEmployer:

    def test_create_job(self,init_database):
        job_created = create_job(1, "Software Development", "Develop software applications.")
        assert job_created is True

    def test_create_job_fail(self,init_database):
        job_created = create_job(999, "Software Development", "Develop software applications.") # Invalid Employer ID
        assert job_created is None

    def test_get_applicants_for_job(self,init_database):
        applicants = get_applicants_for_job(1)  # Job ID 1
        assert applicants is not None
    
    def test_get_applicants_for_job_fail(self,init_database):
        applicants = get_applicants_for_job(999)  # Invalid Job
        assert applicants is None

    def test_review_application_fail(self,init_database):
        review_result = review_application(999, True)  # Invalid Application Reviewing
        assert review_result is None

    def test_review_application(self,init_database):

        review_result = review_application(1, True)  # Application ID 1, accepted
        assert review_result is True
