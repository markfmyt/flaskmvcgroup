import pytest
from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_user,
    get_all_users,
    remove_user,
    remove_job,
    remove_application,
    create_job,
    apply_to_job,
    get_all_jobs,
    view_job_status_all
)

@pytest.fixture(scope="module")
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
    create_user("admin1", "adminpass", "admin1@mail.com", "admin")
    create_user("employer1", "employerpass", "employer1@mail.com", "employer")
    create_user("seeker1", "seekerpass", "seeker1@mail.com", "job_seeker")
    db.session.commit()

class TestAdmin:
    def test_get_all_users(self, test_client, init_database):
      
        users = get_all_users()
        assert users is not None
        assert len(users) == 3

    def test_remove_user(self, test_client, init_database):
 
        create_user("user_to_remove", "userpass", "remove@mail.com", "job_seeker")
        db.session.commit()
        
 
        users_before = get_all_users()
        

        remove_result = remove_user(4)  # the 4th user created
        assert remove_result is True


        users_after = get_all_users()
        assert len(users_after) == len(users_before) - 1

    def test_remove_job(self, test_client, init_database):
        # Create 2 jobs and remove 1
        create_job(2, "Job 1 to remove", "This job will be removed")
        create_job(2, "Job 2 to remove", "This job will be removed")
    
        
        # Remove the job
        remove_result = remove_job(1)  # the first job
        assert remove_result is True

        # Verify the job was removed
        jobs = get_all_jobs()
        assert len(jobs) == 1

    def test_remove_application(self, test_client, init_database):
    
        create_job(2, "Test Job", "This is a test job")
        db.session.commit()
        apply_to_job(3, 3, "Test application")
    
        
        remove_result = remove_application(1)  # This is the first application
        assert remove_result is True

        applications = view_job_status_all(3) # JobSeeker id
        assert applications is None