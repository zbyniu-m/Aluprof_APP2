import jwt
from flask import current_app
from aluprof_app import db
from datetime import datetime, date, timedelta
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    users = db.relationship('User', backref='roles', lazy=True)

    @staticmethod
    def additional_validations(param: str, value: str) -> str:
        return value


class QueryTable(db.Model):
    __tablename__ = 'query_table'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,)
    query_name = db.Column(db.String(255), nullable=True, index=True)
    description = db.Column(db.String(255), nullable=True)
    modification_date = db.Column(db.DateTime, default=datetime.utcnow)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    schedule = db.Column(db.Boolean, nullable=False)
    schedule_interval = db.Column(db.String(1), nullable=True)
    version = db.Column(db.Integer)
    query_string = db.Column(db.Text, nullable=False)
    localization = db.Column(db.String(255), nullable=False)
    restricted = db.Column(db.Boolean, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=True)
    last_creation = db.Column(db.DateTime, nullable=True)
    sql_con = db.Column(db.Integer, nullable=False, default=0)

    def get_def_xlsx_path(self) -> str:
        return os.path.join(self.localization, self.query_name.strip().replace(' ', '_') + '.xlsx')

    def get_list_of_queries(self):
        query_list = self.query_string.split(';')
        for query in query_list:
            if query == '':
                query_list.remove(query)
        return query_list


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False,  unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=1)
    query_tables = db.relationship('QueryTable', backref='owner_tables', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def additional_validations(param: str, value: str) -> date:
        if param == 'creation_date':
            try:
                value = datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                value = None
        return value

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @staticmethod
    def generate_hasgerd_passwort(password: str) -> str:
        return generate_password_hash(password)

    def generate_jwt(self) -> str:
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm="HS256")


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    creation_date = fields.DateTime(dump_only=True)
    role_id = fields.Integer()
    role = fields.Nested(lambda: RoleSchema(only=['id', 'name']))
    query_tables = fields.Nested(lambda: QueryTableSchema(only=['id', 'query_name']))


class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=255))
    users = fields.List(fields.Nested(lambda: UserSchema(exclude=['roles'])))


class UserPasswordUpdateSchema(Schema):
    current_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))


    def __repr__(self):
        return f'{self.query_name}- {self.owner} {self.description}'

class QueryTableSchema(Schema):
    id = fields.Integer(dump_only=True)
    owner = fields.Integer(required=True, validate=validate.Length(max=50))
    query_name = fields.String(validate=validate.Length(max=255))
    description = fields.String(validate=validate.Length(max=255))
    modification_date = fields.Date('%d-%m-%Y')
    creation_date = fields.Date('%d-%m-%Y')
    schedule = fields.Boolean(required=True)
    schedule_interval = fields.String()
    version = fields.Integer()
    query_string = fields.String(required=True)
    localization = fields.String(required=True)
    restricted = fields.Boolean(required=True)
    creation_time = fields.Date('%d-%m-%Y')
    last_creation = fields.Time('%H:%M:%S')
    sql_con = fields.Integer(required=True)

    @validates('schedule_interval')
    def validate_schedule_interval(self, value):
        if str(value) not in ['d', 'w', 'm', 'y']:
            raise ValidationError(f'Schedule musi być wartościa d,w,m lub y')


user_schema = UserSchema()
user_password_update_schema = UserPasswordUpdateSchema()
query_table_schema = QueryTableSchema()
