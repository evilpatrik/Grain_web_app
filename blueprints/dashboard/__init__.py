from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

from . import routes,manager_routes,admin_routes,employee_routes
