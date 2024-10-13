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

class TestEmployer:
    def test_create_job(self):
        # Create an employer
        employer_created = create_user("employer1", "employerpass", "employer1@mail.com", "employer")
        assert employer_created is True

        # Create a job
        job_created = create_job(1, "Software Development", "Develop software applications.")
        assert job_created is True

    def test_get_applicants_for_job(self):
        # Create a job seeker
        job_seeker_created = create_user("seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
        assert job_seeker_created is True

        # Apply to the job
        application_created = apply_to_job(1, 2, "I am interested in this position.")
        assert application_created is True

        # Get applicants for the job
        applicants = get_applicants_for_job(1)  # Job ID 1
        assert applicants is not None
        assert len(applicants) > 0

    def test_review_application(self):
        # Review the application
        review_result = review_application(1, True)  # Application ID 1, accepted
        assert review_result is True

        # Verify the application status
        applicants = get_applicants_for_job(1)
        assert any(app.is_accepted for app in applicants)
