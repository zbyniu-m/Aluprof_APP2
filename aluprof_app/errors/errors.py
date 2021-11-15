from flask import Response, jsonify, redirect, url_for, flash, request, json
from aluprof_app import db, logger
from aluprof_app.errors import errors_bp

class ErrorResponse:
    def __init__(self, message: str, http_status: int):
        self.payload = {
            'success': False,
            'message': message
        }
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        if json.loads(response.data)["message"] == 'The CSRF token has expired.':
            flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'Czas ważności formularza minął, spróbuj ponownie.'
                      , category='warning')
        else:
            flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                          f'{response.status_code}, {json.loads(response.data)["message"]}.\n'
                          , category='Danger')
        return redirect(url_for('index'))

@errors_bp.app_errorhandler(401)
def unauthorized_error(err):
    return ErrorResponse(err.description, 401).to_response()

@errors_bp.app_errorhandler(404)
def not_found_error(err):
    return ErrorResponse(err.description, 404).to_response()


@errors_bp.app_errorhandler(400)
def bad_request_error(err):
    if hasattr(err, 'data'):
        messages = err.data.get('messages', {}).get('json', {})
        return ErrorResponse(messages, 400).to_response()
    return ErrorResponse(err.description,400).to_response()


@errors_bp.app_errorhandler(415)
def unsupported_media_type(err):
    return ErrorResponse(err.description, 415).to_response()


@errors_bp.app_errorhandler(500)
def internal_server_error(err):
    db.session.rollback()
    return ErrorResponse(err.description, 500).to_response()

@errors_bp.app_errorhandler(409)
def conflict_error(err):
    return ErrorResponse(err.description, 409).to_response()