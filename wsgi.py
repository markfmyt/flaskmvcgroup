import click
from flask import Flask, jsonify, request
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from App.database import db, init_db, get_migrate
from App.models import User, Admin, Employer, JobSeeker, Job, Application
from App.controllers import (
    create_user, login_user, review_application,
    view_job_status_all, view_job_status, create_job,
    apply_to_job, get_all_jobs, get_all_users,
    drop_database, remove_application, remove_job, remove_user,
    initialize, get_all_entities, get_applicants_for_job
)
from App.main import create_app

app = create_app()
migrate = get_migrate(app)
jwt = JWTManager(app)
app.debug = True

# CLI command to initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init_db_command():
    initialize()
    print('Database initialized.')

if __name__ == "__main__":
    app.run(port=5000)