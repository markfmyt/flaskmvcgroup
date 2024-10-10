import pytest
from werkzeug.security import check_password_hash
from App.main import create_app
from App.database import db, create_db
from App.models import User, Job, Application
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

# Sample unit tests for User class
class TestUser:
    def test_create_user(self):
        created = create_user("jamal", "jamalpass", "jamal@mail.com", "employer")
        assert created is True

        # Query the database to re-fetch the user
        user = get_user(1)
        assert user is not None
        assert user.username == "jamal"
        assert check_password_hash(user.password, "jamalpass")
        assert user.email == "jamal@mail.com"
        assert user.user_type == "employer"

    def test_update_user(self):
        create_user("ronnie", "ronniepass", "ronnie@mail.com", "admin")
        assert update_user(2, "updated_bob") is True
        
        # Query the database to re-fetch the updated user
        user = get_user(2)
        assert user.username == "updated_bob"

    def test_login_user(self):
        create_user("alice", "alicepass", "alice@mail.com", "job_seeker")
        token = login_user("alice", "alicepass")
        assert token is not None

        # Verify the user exists and has the correct attributes
        user = get_user(3)
        assert user.username == "alice"
        assert check_password_hash(user.password, "alicepass")
        assert user.email == "alice@mail.com"

class TestJob:
    def test_create_job(self):
        create_user("employer1", "employerpass", "employer1@mail.com", "employer")
        user = get_user(4)
        job_created = create_job(4, "Software Development", "Develop software applications.")
        assert job_created is True

        # Query the database to re-fetch the job
        job = Job.query.filter_by(id=1, employer_id = 4).first()
        assert job is not None
        assert job.category == "Software Development"
        assert job.description == "Develop software applications."

        user = get_user(4)
        assert user.username == "employer1"
        assert check_password_hash(user.password, "employerpass")
        assert user.email == "employer1@mail.com"
        

    def test_apply_to_job(self):
        create_user("job_seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
        job_seeker = User.query.filter_by(username = "job_seeker1").first()

        job = Job.query.filter_by(id=1, employer_id = 4).first()
        application_result = apply_to_job(job.id, job_seeker.id, "I am a skilled software developer.")

        assert application_result is True

        # Query the database to re-fetch the application
        application = Application.query.filter_by(job_id=job.id, job_seeker_id=job_seeker.id).first()
        assert application is not None
        assert application.application_text == "I am a skilled software developer."

    def test_view_job_status_all(self):
        applications = view_job_status_all(User.query.filter_by(username = "job_seeker1").first().id)
        assert applications is not None

        # Ensure at least one application exists
        assert len(applications) > 0

    def test_review_application(self):
        job = Job.query.filter_by(id=1, employer_id = 4).first()
        job_seeker = User.query.filter_by(username = "job_seeker1").first()

        application = Application.query.filter_by(job_seeker_id = job_seeker.id, job_id = job.id).first()
        review_result = review_application(application.application_id, True)
        assert review_result is True

        check_application = Application.query.filter_by(application_id=application.application_id).first()
        assert check_application is not None
        assert check_application.is_accepted is True

# Sample tests for removal functions
class TestRemoval:
    def test_remove_user(self):
        user_created = create_user("user_to_remove", "pass", "email@mail.com", "employer")
        retrieve_created_user = User.query.filter_by(username = "user_to_remove").first()
        created_user_id = retrieve_created_user.id
        assert remove_user(created_user_id) is True

        # Query the database to confirm the user was removed
        user = get_user(created_user_id)
        assert user is None

    def test_remove_application(self):
        job = Job.query.filter_by(id=1, employer_id = 4).first()
        job_seeker = User.query.filter_by(username = "job_seeker1").first()

        application = Application.query.filter_by(job_seeker_id = job_seeker.id, job_id = job.id).first()
        assert remove_application(application.application_id) is True  # Remove application with ID 1
        assert Application.query.filter_by(job_seeker_id = job_seeker.id, job_id = job.id).first() is None

    def test_remove_job(self):
        job_to_remove = Job.query.filter_by(id=1, employer_id = 4).first()
        assert remove_job(job_to_remove.id) is True 
         
        job_after_remove = Job.query.filter_by(id=1, employer_id = 4).first()
        assert job_after_remove is None

