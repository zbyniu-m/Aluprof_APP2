import jwt
import re
from flask import request, url_for, current_app, abort
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from flask_sqlalchemy import DefaultMeta, BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
from typing import Tuple
from pandas import pandas as pd
from urllib.parse import urlparse, urljoin
from config import cx_connection
import os

COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(gte|gt|lte|lt)]')


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType('Content type must by application/json')
        return func(*args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')
        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description='Missing token. Please login or register')

        try:
            payload = jwt.decode(jwt=token, key=current_app.config.get('SECRET_KEY'), algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            abort(401, description='Expired token. Please login to get new token')

        except jwt.InvalidTokenError:
            abort(401, description='Invalid token. Please login or register')
        else:
            return func(payload['user_id'], *args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated or current_user.role_id != 2:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def get_schema_args(model: DefaultMeta) -> dict:
    schema_args = {'many': True}
    fields = request.args.get('fields')
    if fields:
        schema_args['only'] = [field for field in fields.split(',') if field in model.__table__.columns]
    return schema_args


def apply_orders(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    sort_keys = request.args.get('sort')
    if sort_keys:
        for key in sort_keys.split(','):
            desc = False
            if key.startswith('-'):
                key = key[1:]
                desc = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
    return query


def _get_filter_argument(column_name: InstrumentedAttribute, value: str, operator: str) -> BinaryExpression:
    operator_mapping = {
        '==': column_name == value,
        'gte': column_name >= value,
        'gt': column_name > value,
        'lte': column_name <= value,
        'lt': column_name < value
        }
    return operator_mapping[operator]


def apply_filter(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    for param, value in request.args.items():
        if param not in {'fields', 'sort', 'page', 'limit'}:
            operator = '=='
            match = COMPARISON_OPERATORS_RE.match(param)
            if match is not None:
                param, operator = match.groups()
            column_attr = getattr(model, param, None)
            if column_attr is not None:
                value = model.additional_validations(param, value)
                if value is None:
                    continue
                filter_argument = _get_filter_argument(column_attr, value, operator)
                query = query.filter(filter_argument)
    return query


def get_pagination(query: BaseQuery, func_name: str) -> Tuple[list, dict]:
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config.get('PER_PAGE', 10), type=int)
    params = {key: value for key, value in request.args.items() if key != 'page'}
    pagintate_obj = query.paginate(page, limit, False)
    pagination = {
            'total_pages': pagintate_obj.pages,
            'total_records': pagintate_obj.total,
            'curent_page': url_for(func_name, page=page, **params)
        }
    if pagintate_obj.has_next:
        pagination['next_page'] = url_for(func_name, page=page + 1, **params)
    if pagintate_obj.has_prev:
        pagination['previous_page'] = url_for(func_name, page=page - 1, **params)

    return pagintate_obj.items, pagination


def oracle_query_to_dict(query: str) -> Tuple[list, dict]:
    df = pd.read_sql_query(query, cx_connection)
    headers = [{'name': col} for col in df.columns]
    data = df.to_dict('records')
    return headers, data


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def dataframe_to_excel(df: list, path: str, sheet_name: str):
    # Saving dataframe to Excel
    numerator = 0
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for data in df:
        if isinstance(data, pd.DataFrame):
            sheet_name = sheet_name.strip().replace(' ', '_')
            if len(sheet_name) > 20:
                sheet_name = sheet_name[:20]+str(numerator)
            else:
                sheet_name = sheet_name + str(numerator)
            data.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)
            # Preparing table obj in excel:
            # Get the xlsxwriter workbook and worksheet objects.

            worksheet = writer.sheets[sheet_name]

            # Get the dimensions of the dataframe.
            (max_row, max_col) = data.shape

            # Create a list of column headers, to use in add_table().
            column_settings = []
            for header in data.columns:
                column_settings.append({'header': header})

            # Add the table.
            worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'name': sheet_name})

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)

            numerator = numerator+1
    writer.save()


def get_dataframe_from_query_list(queries, connection):
    df = []
    # preparing list of dataframe from list of queries
    for query in queries:
        if query:
            query = query.strip()
            df.append(pd.read_sql_query(query, connection))
    return df


def create_dir_if_not_exists(path) -> bool:
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False
