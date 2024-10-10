import pytest
from App.main import create_app
from App.database import db
from App.models import User, Job, JobSeeker, Admin, Employer, Application
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def app():
    """Create a Flask application for the tests."""
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def init_db(app):
    """Initialize the database for tests."""
    with app.app_context():
        db.create_all()
        yield db  
        db.session.remove()
        db.drop_all()


@pytest.fixture
def create_user(app, init_db):  
    """Fixture to create a user for testing."""
    user = User(
        username='test_user',
        password=generate_password_hash('test_password'),
        email='test_user@example.com',
        user_type='job_seeker'
    )
    
    with app.app_context():  
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user



@pytest.fixture
def create_application(app, init_db):
    """Fixture to create a job, job seeker, and application for testing."""

    with app.app_context():

        employer = Employer(
            username='test_employer',
            password=generate_password_hash('test_password'),
            email='employer@example.com',
            company_name='Test Company'
        )
        db.session.add(employer)
        db.session.commit()
        db.session.refresh(employer)

        job = Job(
            category='Engineering',
            description='Test Job Description',
            employer_id=employer.id
        )
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)

        job_seeker = JobSeeker(
            username='test_job_seeker',
            password=generate_password_hash('test_password'),
            email='job_seeker@example.com'
        )
        db.session.add(job_seeker)
        db.session.commit()
        db.session.refresh(job_seeker)
       
        application = Application(
            job_seeker_id=job_seeker.id,
            job_id=job.id,
            application_text='Test application text'
        )
        db.session.add(application)
        db.session.commit()
        db.session.refresh(application)
        return application


@pytest.fixture
def admin_client(client, init_db):
    """Create a client for testing as an admin user."""
    with client.application.app_context():
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                password=generate_password_hash('password'),
                email='admin@example.com',
                user_type='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            db.session.refresh(admin_user)

        token = create_access_token(identity=admin_user.username)
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    return client



# Your tests
def test_list_users(admin_client):
    """Test listing users as an admin client."""
    response = admin_client.get('/api/users')
    assert response.status_code == 200
    assert 'users' in response.json  # Check if 'users' exists
    assert isinstance(response.json['users'], list)  # Ensure it's a list





def test_remove_user(admin_client, create_user):
    """Test removing a user as an admin client."""

    user_to_delete = create_user  
    assert user_to_delete is not None
    response = admin_client.delete(f'/api/admin/remove_user/{user_to_delete.id}')
    assert response.status_code == 200
    response = admin_client.get(f'/api/users')
    users_list = response.get_json().get("users", [])
    assert all(user['id'] != user_to_delete.id for user in users_list)
    response = admin_client.get(f'/api/users/{user_to_delete.id}')
    assert response.status_code == 404 




def test_print_all_entities(admin_client):
    response = admin_client.get('/api/admin/print_all')
    
    assert response.status_code == 200
    data = response.get_json()

    assert "users" in data
    assert "jobs" in data

    for user in data["users"]:
        assert "id" in user
        assert "username" in user
        assert "email" in user

    for job in data["jobs"]:
        assert "id" in job
        assert "title" in job
        assert "description" in job





def test_remove_application(admin_client, create_application):
    """Test the admin's ability to remove an application."""

    application_to_delete = create_application
    assert application_to_delete is not None
    application_to_delete = Application.query.get(application_to_delete.application_id)
    assert application_to_delete is not None
    response = admin_client.delete(f'/api/admin/remove_application/{application_to_delete.application_id}')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Application removed successfully."}
    deleted_application = Application.query.get(application_to_delete.application_id)
    assert deleted_application is None




def test_remove_job(admin_client):
    """Test the admin's ability to remove a job."""

    employer = Employer(
        username="employer123",
        password="password123",
        email="employer123@example.com",
        company_name="Tech Solutions"
    )
    db.session.add(employer)
    db.session.commit()
    job = Job(
        category="Software Development",
        description="A job for software developers",
        employer_id=employer.id
    )
    db.session.add(job)
    db.session.commit()
    job_to_delete = Job.query.get(job.id)
    assert job_to_delete is not None
    response = admin_client.delete(f'/api/admin/remove_job/{job_to_delete.id}')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Job removed successfully."}
    deleted_job = Job.query.get(job_to_delete.id)
    assert deleted_job is None

