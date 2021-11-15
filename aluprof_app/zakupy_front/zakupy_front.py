from flask import  render_template
from aluprof_app.zakupy_front import zakupy_front_bp


@zakupy_front_bp.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')


