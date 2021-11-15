import logging
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
db = SQLAlchemy()
login_manager= LoginManager()
migrate = Migrate()
#definiowanie ustawień loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_app(config_name='development'):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_object(config[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    db.app = app

    #from aluprof_app.commands import db_manage_bp
    from aluprof_app.errors import errors_bp
    from aluprof_app.auth import auth_bp
    from aluprof_app.zakupy_front import zakupy_front_bp

    csrf.exempt(errors_bp)
    csrf.exempt(auth_bp)

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(zakupy_front_bp, url_prefix='/zakupy')
    logger.info(
        f'Aplikacja utworzona w trybie: {config_name}')

    @app.route('/', methods=['POST', 'GET'])
    def index():
        return redirect(url_for('zakupy_front.index'))

    return app
