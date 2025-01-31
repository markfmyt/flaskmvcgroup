# blue prints are imported 
# explicitly instead of using *
from .index import index_views
from .admin import setup_admin
from .job_seeker import job_seeker_views
from .everyone import everyone_views
from .employer import employer_views
from .admins import admin_views

views = [index_views, job_seeker_views, everyone_views, employer_views, admin_views] 
# blueprints must be added to this list