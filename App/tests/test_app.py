import pytest
from werkzeug.security import generate_password_hash
from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, JobSeeker, Admin
from App.controllers import (
    create_user,
    get_all_users_json,
    login_user,
    get_user,
    update_user,
    apply_to_job,
    view_job_status_all,
    create_job,
    review_application,
    remove_user,
    remove_job,
    remove_application
)

@pytest.fixture(autouse=True, scope="module")
def test_client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Sample unit tests for User
class TestUser:
    def test_create_user(self):
        user = create_user("jamal", "jamalpass", "jamal@mail.com", "employer")
        assert user is True

    def test_update_user(self):
        create_user("ronnie", "ronniepass", "ronnie@mail.com", "admin")
        assert update_user(1, "updated_bob") is True  # Update first user
        user = get_user(1)
        assert user.username == "updated_bob"

    def test_login_user(self):
        create_user("alice", "alicepass", "alice@mail.com", "job_seeker")
        token = login_user("alice", "alicepass")
        assert token is not None

class TestJob:
    def test_create_job(self):
        create_user("employer1", "employerpass", "employer1@mail.com", "employer")
        job_created = create_job(1, "Software Development", "Develop software applications.")
        assert job_created is True  # Assuming create_job returns True on success

    def test_apply_to_job(self):
        create_user("job_seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
        job_created = create_job(1, "Software Development", "Develop software applications.")
        application_result = apply_to_job(1, 1, "I am a skilled software developer.")
        assert application_result is True

    def test_view_job_status_all(self):
        applications = view_job_status_all(1)  # Assuming job seeker ID 1
        assert applications is not None  # Assuming there are applications

    def test_review_application(self):
        application_id = 1  # Assuming this ID exists
        review_result = review_application(application_id, True)
        assert review_result is True

# Sample tests for removal functions
class TestRemoval:
    def test_remove_user(self):
        user_created = create_user("user_to_remove", "pass", "email@mail.com", "employer")
        assert remove_user(1) is True  # Remove user with ID 1

    def test_remove_job(self):
        job_created = create_job(1, "To Be Removed", "Remove this job")
        assert remove_job(1) is True  # Remove job with ID 1

    def test_remove_application(self):
        # Ensure there's a job and user before creating an application
        create_user("job_seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
        create_job(1, "Test Job", "This is a job to apply for.")
        
        # Create an application before testing its removal
        application_result = apply_to_job(1, 1, "This is a test application")
        assert application_result is True  # Ensure the application was created successfully
        
        # Now test removing the application
        assert remove_application(1) is True  # Remove application with ID 1
