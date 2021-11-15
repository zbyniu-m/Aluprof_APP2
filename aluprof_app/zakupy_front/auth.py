from flask import render_template, flash, redirect, request, url_for
from flask_wtf import FlaskForm
from aluprof_app.zakupy_front import zakupy_front_bp
from aluprof_app.models import User, Role, UserSchema, RoleSchema
from aluprof_app.utils import is_safe_url, get_schema_args, apply_orders, get_pagination, apply_filter, admin_required
from aluprof_app import db, login_manager, logger
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import Email, InputRequired, EqualTo
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from faker import Faker

class LoginForm(FlaskForm):
    username = StringField(label='Nazwa użytkownika', id='user-name')
    email = StringField(label='E-mail', validators=[Email()], id='inlineFormInputName')
    password = PasswordField(label='Hasło', id='inlineFormInputGroundUsername')
    remember = BooleanField(label='Zapamiętaj mnie')

class PasswordChangingForm(FlaskForm):
    old_password = PasswordField(label='Stare hasło:', id='old_password', validators=[InputRequired(message='Pole musi być uzupełnione.')])
    new_password = PasswordField(label='Nowe hasło:', id='old_password', validators=[InputRequired(message='Pole musi być uzupełnione.'), EqualTo('new_2_password', message='Nowe i powtórzone hasło muszą być takie same.')])
    new_2_password = PasswordField(label='Powtórz nowe hasło:', id='old_password', validators=[InputRequired(message='Pole musi być uzupełnione.')])

class CreateUserForm(FlaskForm):
    username = StringField(label='Nazwa użytkownika', id='user-name', validators=[InputRequired(message='Pole musi być uzupełnione.')])
    email = StringField(label='E-mail', validators=[Email(), InputRequired(message='Pole musi być uzupełnione.')], id='inlineFormInputName')
    password = PasswordField(label='Hasło:', id='password', validators=[InputRequired(message='Pole musi być uzupełnione.'), EqualTo('repeat_password', message='Hasło i powtórzone hasło muszą być takie same.')])
    repeat_password = PasswordField(label='Powtórz hasło:', id='passwor_reapet', validators=[InputRequired(message='Pole musi być uzupełnione.')])
    role =  SelectField(label='Rola', coerce=int)


@zakupy_front_bp.route('/init', methods=['POST', 'GET'])
def init():
    role_common = Role.query.filter(Role.name == 'common').first()
    if role_common == None:
        role_common = Role(id=1, name='common')
        db.session.add(role_common)
        db.session.commit()
        print('added common role')

    role_admin = Role.query.filter(Role.name == 'admin').first()
    if role_admin == None:
        role_admin = Role(id=2, name='admin')
        db.session.add(role_admin)
        db.session.commit()
        print('added admin role')
    role_keyuser = Role.query.filter(Role.name == 'keyuser').first()
    if role_keyuser == None:
        role_admin = Role(id=3, name='keyuser')
        db.session.add(role_admin)
        db.session.commit()
        print('added admin role')

    admin = User.query.filter(User.username == 'admin').first()
    if admin == None:
        admin = User(username='admin',
                     password=generate_password_hash('xyz'),
                     email='zbyniu.m@gmail.com',
                     role_id=2
                     )
        print('created admin user')
        db.session.add(admin)
        db.session.commit()

    return '<h1>Inicjalizacja zakończona</h1>'

@zakupy_front_bp.route('/init_fake', methods=['POST', 'GET'])
def init_fake_data():
    faker = Faker()
    for x in range(20):
        user = User(username=faker.name(),
                     password=generate_password_hash('xyz'),
                     email=faker.ascii_email(),
                     role_id=1
                     )
        db.session.add(user)
    db.session.commit()
    return '<h1>Inicjalizacja danych testowych zakończona</h1>'



@zakupy_front_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter(User.email == form.email.data).first()
            logger.info(
                f'{request.host_url}: Proces logowania: {user.username}')
            if user != None and user.is_password_valid(password=form.password.data):
                login_user(user, remember=form.remember.data)
                print('logowanie ok')

                next = request.args.get('next')
                if next and is_safe_url(next):
                    flash(message=f'Logowanie zakończyło się sukcesem. Witaj {current_user.username}', category='success')
                    return redirect(next)
                else:
                    flash(message=f'Logowanie zakończyło się sukcesem. Witaj {current_user.username}', category='success')
                    return redirect('/zakupy')
            else:
                logger.debug(
                    f'{request.host_url}: Proces logowania - dane niepoprawne: {user.username}')
                flash(message='Dane logowania są niepoprawne.', category='danger')

        return render_template('login.html', form=form)
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces logowania przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


@zakupy_front_bp.route('/logout')
def logout():
    logout_user()
    flash(message=f'Wylogowanie zakończyło się sukcesem', category='success')
    return redirect('/zakupy')

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()

@zakupy_front_bp.route('/user', methods=['POST', 'GET'])
@login_required
def user_account():
    try:
        user = User.query.filter(User.id == current_user.id).first()
        password_changening_form = PasswordChangingForm()
        if user is not None:
            form = LoginForm()
            form.email.data = user.email
            form.username.data = user.username
            form.password.data = ''
            form.remember.data = False
            if password_changening_form.validate_on_submit() and user.is_password_valid(password_changening_form.old_password.data):
                logger.debug(
                    f'{request.host_url}: Proces zmiany hasła: {user.username}')
                user.password = user.generate_hasgerd_passwort(password_changening_form.new_password.data)
                db.session.commit()
                flash(message='Hasło zostało zmienione.', category='success')
            return render_template('user.html', form=form, form2=password_changening_form, kto='Twoje dane:')
        else:
            return redirect('/zakupy')
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces user_account przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))

@zakupy_front_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        query = User.query.filter(User.role_id != 2)
        schema_args = get_schema_args(User)
        query = apply_orders(User, query)
        query = apply_filter(User, query)
        items, pagination = get_pagination(query, 'zakupy_front.get_users')
        users = UserSchema(**schema_args).dump(items)
        return render_template('users.html',
                               users=users,
                               pagination=pagination,
                               number_of_records=len(users))
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces get_users przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


@zakupy_front_bp.route('/users/del:<int:user_id>', methods=['GET'])
@admin_required
def deleted_user(user_id: int):
    try:
        user = User.query.get_or_404(user_id, description=f'User with id {user_id} not found')
        db.session.delete(user)
        db.session.commit()
        flash(f'Usunięto użytkownika {user.username}', category='success')
        return redirect('/zakupy/users')
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces deleted_user przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))

@zakupy_front_bp.route('/users/edit:<int:user_id>', methods=['GET','POST'])
@admin_required
def edit_user(user_id: int):
    try:
        print(f'id edytowanego użytkownia: {user_id}')
        user = User.query.filter(User.id == user_id).first()
        print(user)
        password_changening_form = PasswordChangingForm()
        password_changening_form.new_password.validators
        if user is not None:
            form = LoginForm()
            form.email.data = user.email
            form.username.data = user.username
            form.password.data = ''
            form.remember.data = False
            if password_changening_form.is_submitted():
                user.password = user.generate_hasgerd_passwort(password_changening_form.new_password.data)
                db.session.commit()
                flash(message='Hasło zostało zmienione.', category='Success')
            return render_template('user.html', form=form, form2=password_changening_form, kto='Edycja użytkownika:')
        else:
            return redirect('/zakupy/users')
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces edit_user przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))

@zakupy_front_bp.route('/users/create_user', methods=['GET','POST'])
@admin_required
def create_user():
    try:
        form = CreateUserForm()
        form.role.choices = [(g.id, g.name) for g in Role.query.order_by('id')]
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user is not None:
                flash(f'Użytkownik {form.username.data} już istnieje', category='danger')
                return render_template('create_user.html', form=form)
            user = User.query.filter(User.email == form.email.data).first()
            if user is not None:
                flash(f'Email {form.email.data} już istnieje w bazie', category='danger')
                return render_template('create_user.html', form=form)
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password.data),
                        email=form.email.data,
                        role_id=form.role.data
                        )
            db.session.add(user)
            db.session.commit()
            flash(f'Utworzono nowego użytkownika {user.username}', category='success')
            return redirect('/zakupy/users')
        return render_template('create_user.html', form=form)
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces create_user przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


