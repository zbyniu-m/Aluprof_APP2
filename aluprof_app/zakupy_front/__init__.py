from flask import Blueprint
from aluprof_app import login_manager

login_manager.login_view = 'zakupy_front.login'
login_manager.login_message = 'Dostęp chroniony. Proszę zaloguj się.'
zakupy_front_bp = Blueprint('zakupy_front', __name__, static_folder='static', template_folder='templates')

from aluprof_app.zakupy_front import zakupy_front
from aluprof_app.zakupy_front import bomorozbijacz
from aluprof_app.zakupy_front import cenniki
from aluprof_app.zakupy_front import raports_to_xlsx
from aluprof_app.zakupy_front import auth
from aluprof_app.zakupy_front import schedules
