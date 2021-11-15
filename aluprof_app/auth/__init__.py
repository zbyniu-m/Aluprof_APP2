from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from aluprof_app.auth import auth