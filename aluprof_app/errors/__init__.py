from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from aluprof_app.errors import errors
