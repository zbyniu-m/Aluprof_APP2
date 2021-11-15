import os.path
from flask import render_template, redirect, url_for, flash, request, current_app
from aluprof_app import db, logger
from config import connections
from aluprof_app.zakupy_front import zakupy_front_bp
from flask_login import login_required, current_user
from aluprof_app.models import QueryTable, User
from aluprof_app.utils import admin_required, dataframe_to_excel, get_dataframe_from_query_list, create_dir_if_not_exists
from flask_wtf import FlaskForm
from wtforms import StringField,  BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length
from datetime import datetime, timedelta
import time

con_choises = []
for con in connections:
    con_choises.append((con['id'], con['name']))
    print(con['id'])

class NewReport(FlaskForm):
    owner = SelectField(label='Raport dostępny dla użytkownika:',
                        validators=[InputRequired(), Length(max=50, message='Maksymalna ilość zanków to 50')])
    query_name = StringField(label='Nazwa:', validators=[Length(max=255, message='Maksymalna ilość zanków to 255')])
    description = StringField(label='Opis:', validators=[Length(max=255, message='Maksymalna ilość zanków to 255')])
    schedule = BooleanField(label='harmonogramowany')
    schedule_interval = SelectField(label='Cykl harmonogramu:',
                                    choices=[('d', 'dzienny'),
                                             ('w', 'tygodniowy'),
                                             ('m', 'miesięczny'),
                                             ('y', 'roczny')])
    version = IntegerField(label='Wersja:', validators=[InputRequired(message='To pole musi zostać uzupełnione.')])
    query_text = TextAreaField(label='Zapytanie SQL:',
                               validators=[InputRequired(message='To pole musi zostać uzupełnione.')])
    localization = StringField(label='Lokalizacja pliku:')
    restricted = BooleanField('chroniony')
    sql_connection = SelectField(label='Baza danych zapytania:',
                                 choices=con_choises)


@zakupy_front_bp.route('/raports_to_xlsx', methods=['POST', 'GET'])
@login_required
def raports_to_xlsx():
    try:
        if current_user.role_id == 1:
            raport = QueryTable.query.filter(QueryTable.owner == current_user.id).order_by(QueryTable.owner).all()
        else:
            raport = QueryTable.query.order_by(QueryTable.owner).all()
        return render_template('raports_to_xlsx.html', list_of_raports=raport)
    except Exception as err:
        logger.error(
            f'{request.host_url}: zalogowany użytkownik: '
            f'{current_user.username} wczytywanie raportów do tabeli, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


@zakupy_front_bp.route('/raports_to_xlsx/<int:raport_id>', methods=['POST', 'GET'])
@login_required
def make_raport(raport_id: int):
    logger.info(f'{request.host_url}: tworzenie raportu o id: {raport_id}')
    try:
        raport = QueryTable.query.filter(QueryTable.id == raport_id).first()
        if raport:
            start_time = time.time()
            lokalizacja = raport.localization
            if create_dir_if_not_exists(lokalizacja):
                logger.info(f'utworzono katalog {lokalizacja}')

            queries = raport.get_list_of_queries()
            # preparing list of dataframe from list of queries
            if connections[raport.sql_con]['connection']:
                con = connections[raport.sql_con]['connection']
            else:
                con = connections[0]['connection']
            df = get_dataframe_from_query_list(queries, con)

            path = raport.get_def_xlsx_path()
            sheet_name = raport.query_name.strip().replace(' ', '_')

            # Saving dataframe to Excel
            dataframe_to_excel(df, path, sheet_name)

            end_time = time.time()

            # Saving parameters to database
            duration = end_time-start_time
            raport.creation_time = datetime.strptime(str(timedelta(seconds=round(duration))), "%H:%M:%S")
            raport.last_creation = datetime.now()
            db.session.commit()

            # return information to page
            flash(message=f'Utworzono raport w lokalizacji: {raport.localization}', category='success')
            return redirect(url_for('zakupy_front.raports_to_xlsx'))
        else:
            flash(message=f'Raport o id: {raport.id} nieistnieje.', category='danger')
            return redirect(url_for('zakupy_front.raports_to_xlsx'))
    except IOError as err:
        logger.error(
            f'{request.host_url}: zalogowany użytkownik: {current_user.username} tworzenie raportu o '
            f'id: {raport_id}, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd. '
                      f'Sprawdź czy plik, który próbujesz utworzyć jest otwarty. '
                      f'Spróbuj ponownie jak będzie zamknięty.', category='danger')
        return redirect(url_for('zakupy_front.index'))
    except Exception as err:
        logger.error(f'{request.host_url}: zalogowany użytkownik: {current_user.username} '
                     f'tworzenie raportu o id: {raport_id}, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.raports_to_xlsx'))


@zakupy_front_bp.route('/raports_to_xlsx/new', methods=['POST', 'GET'])
@admin_required
def add_raports():
    form = NewReport()
    form.owner.choices = [(
        g.id,
        g.username)
        for g in User.query.with_entities(
        User.id,
        User.username
    ).order_by(User.username)]
    try:
        if form.validate_on_submit():
            if form.localization.data:
                lokalizacja = form.localization.data
            else:
                user = User.query.filter(User.id == form.owner.data).first()
                lokalizacja = os.path.join(current_app.config.get('DEF_DIR'),
                                           user.username.strip().replace(' ', '_'))
                if not os.path.exists(lokalizacja):
                    os.makedirs(lokalizacja)
            print(lokalizacja)
            query = QueryTable(
                    owner=form.owner.data,
                    query_name=form.query_name.data,
                    description=form.description.data,
                    modification_date=datetime.now(),
                    creation_date=datetime.now(),
                    schedule=form.schedule.data,
                    schedule_interval=form.schedule_interval.data,
                    version=form.version.data,
                    query_string=f'{form.query_text.data}',
                    localization=lokalizacja,
                    restricted=form.restricted.data,
                    sql_con=int(form.sql_connection.data)
            )

            logger.info(f'{request.host_url}: dodawanie nowego raportu {query.query_name} ')
            db.session.add(query)
            db.session.commit()
            flash(message=f'Dodano zapytanie {query.query_name} do bazy danych', category='success')
            return redirect(url_for('zakupy_front.raports_to_xlsx'))
        return render_template('new_report.html', form=form, title='Nowy raport')
    except Exception as err:
        logger.error(
            f'{request.host_url}: zalogowany użytkownik: {current_user.username} dodawanie nowego raportu, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


@zakupy_front_bp.route('/raports_to_xlsx/edit:<int:raport_id>', methods=['POST', 'GET'])
@admin_required
def edit_raports(raport_id: int):
    try:
        raport = QueryTable.query.filter(QueryTable.id == raport_id).first()
        form = NewReport()
        form.sql_connection.choices = con_choises
        form.owner.choices = [(g.id, g.username) for g in
                              User.query.with_entities(User.id, User.username).order_by(User.username)]
        title = 'Edycja raportu'
        if raport:
            if form.validate_on_submit():
                logger.info(f'{request.host_url}: edytowanie raportu {raport_id} ')
                raport.owner = form.owner.data
                raport.query_name = form.query_name.data
                raport.description = form.description.data
                raport.modification_date = datetime.now()
                raport.creation_date = raport.creation_date
                raport.schedule = form.schedule.data
                raport.schedule_interval = form.schedule_interval.data
                raport.version = form.version.data
                raport.query_string = f'{form.query_text.data}'
                raport.localization = form.localization.data
                raport.restricted = form.restricted.data
                raport.sql_con = int(form.sql_connection.data)
                logger.info(f'{request.host_url}: edytowanie  raportu {raport.query_name} ')
                db.session.commit()
                flash(message=f'Zmieniono zapytanie {raport.query_name} w bazie danych', category='success')
                return redirect(url_for('zakupy_front.raports_to_xlsx'))
            else:
                form.sql_connection.data = str(raport.sql_con)
                form.localization.data = raport.localization
                form.version.data = raport.version
                form.restricted.data = raport.restricted
                form.query_name.data = raport.query_name
                form.owner.data = raport.owner
                form.description.data = raport.description
                form.schedule_interval.data = raport.schedule_interval
                form.schedule.data = raport.schedule
                form.query_text.data = raport.query_string
        return render_template('new_report.html', form=form, title=title)
    except Exception as err:
        logger.error(
            f'{request.host_url}: zalogowany użytkownik: {current_user.username} '
            f'edycja raportu {raport_id}, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))


@zakupy_front_bp.route('/raports_to_xlsx/del:<int:raport_id>', methods=['POST', 'GET'])
@admin_required
def delete_raport(raport_id: int):
    try:
        raport = QueryTable.query.filter(QueryTable.id == raport_id).first()
        if raport:
            logger.info(f'{request.host_url}: usuwanie raportu {raport.query_name} ')
            db.session.delete(raport)
            db.session.commit()
            flash(message=f'Usunięto zapytanie {raport.query_name} z bazy danych', category='success')
        return redirect(url_for('zakupy_front.raports_to_xlsx'))
    except Exception as err:
        logger.error(
            f'{request.host_url}: zalogowany użytkownik: {current_user.username} '
            f'usuwanie raportu {raport_id}, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))
