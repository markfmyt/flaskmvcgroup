# Job Application System REST API

This is a Flask-based Job Application System that provides a REST API for managing job listings, applications, and user accounts. The system supports three types of users: Job Seekers, Employers, and Admins.

## Features

- User authentication and authorization
- Job listing creation and management
- Job application submission and review
- User role-based access control (Admin, Employer, Job Seeker)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/markfmyt/flaskmvcgroup
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the database and run:
   ```
   flask init
   flask run
   ```

## API Endpoints

### Authentication

- `POST /api/users/login`: User login
- `POST /api/users/signup`: User signup
- `GET /api/users/logout`: User logout

### Job Listings

- `GET /api/jobs`: List all job postings
- `POST /api/employer/create_job`: Create a new job listing (Employer only)

### Job Applications

- `POST /api/jobs/apply`: Apply for a job (Job Seeker only)
- `GET /api/jobs/applications`: View all applications by a Job Seeker
- `GET /api/jobs/status/<application_id>`: View status of a specific application
- `POST /api/employer/review/<application_id>`: Review an application (Employer only)

### Admin Operations

- `DELETE /api/admin/remove_user/<user_id>`: Remove a user (Admin only)
- `DELETE /api/admin/remove_job/<job_id>`: Remove a job listing (Admin only)
- `DELETE /api/admin/remove_application/<application_id>`: Remove an application (Admin only)
- `GET /api/users`: List all users (Admin only)

## Typical Usage

To interact with the API, you can use tools like cURL, Postman, or any HTTP client library. Here are some example requests:

1. Employer Signup:
   ```
   POST /api/users/signup
   {
     "username": "microsoft",
     "password": "billgates1",
     "email": "billgates@mail.com",
     "role": "employer"
   }
   ```

2. Job Seeker Signup:
   ```
   POST /api/users/signup
   {
     "username": "bob",
     "password": "bobpass1",
     "email": "bob@mail.com",
     "role": "job_seeker"
   }
   ```

3. Employer Login:
   ```
   POST /api/users/login
   {
     "username": "microsoft",
     "password": "billgates1"
   }
   ```

4. Create a Job Listing (Employer):
   ```
   POST /api/employer/create_job
   Authorization: Bearer <access_token>
   {
     "category": "Software Engineer",
     "description": "Looking for a backend developer with React experience"
   }
   ```

5. Job Seeker Login:
   ```
   POST /api/users/login
   {
     "username": "bob",
     "password": "bobpass1"
   }
   ```

6. Apply for a Job (Job Seeker):
   ```
   POST /api/jobs/apply
   Authorization: Bearer <access_token>
   {
     "job_id": 1,
     "application_text": "I have 5 years of experience in backend development with React."
   }
   ```

7. Review an Application (Employer):
   ```
   POST /api/employer/review/1
   Authorization: Bearer <access_token>
   {
     "decision": "accept"
   }
   ```

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. Include the access token in the `Authorization` header of your requests:

```
Authorization: Bearer <access_token>
```

## Error Handling

The API returns appropriate HTTP status codes and error messages in JSON format:

```json
{
  "error": "Error message description"
}
```

## Database Schema

The application uses SQLAlchemy with the following main models:
- User (base class for Admin, Employer, and JobSeeker)
- Job
- Application


## Testing

To run the test suite, in the console:

```
pytest
```

## Credits

This project is based on the [FlaskMVC Template](https://github.com/uwidcit/flaskmvc).
