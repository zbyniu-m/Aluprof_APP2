from flask import render_template
from aluprof_app import scheduler, logger, db
from aluprof_app.models import QueryTable
from aluprof_app.utils import create_dir_if_not_exists, get_dataframe_from_query_list, dataframe_to_excel, admin_required
from aluprof_app.zakupy_front import zakupy_front_bp
from flask_wtf import FlaskForm
from wtforms.fields.html5 import TimeField
from wtforms import BooleanField
from wtforms.validators import InputRequired, Length
from sqlalchemy import extract
from config import connections, schedule_time
import datetime
import time

report_on_schedule_time = datetime.datetime.strptime(schedule_time, '%H:%M')

def create_reports_on_schedule():
    try:
        # get reports from database
        daily_reports = QueryTable.query.filter(QueryTable.schedule == True,
                                                QueryTable.schedule_interval == 'd').all()

        logger.info(f'schedule: create_reports_on_schedule  ilość raportów dziennych: {len(daily_reports)}')

        week_ago = datetime.datetime.now()-datetime.timedelta(6.9)

        weekly_reports = QueryTable.query.filter(QueryTable.schedule == True,
                                                 QueryTable.schedule_interval == 'w',
                                                 QueryTable.last_creation <= week_ago).all()

        logger.info(f'schedule: create_reports_on_schedule  ilość raportów tygodniowych: {len(weekly_reports)}')

        monthly_reports = QueryTable.query.filter(QueryTable.schedule == True,
                                                  QueryTable.schedule_interval == 'm',
                                                  extract('month', QueryTable.last_creation) < datetime.datetime.now().month).all()

        logger.info(f'schedule: create_reports_on_schedule  ilość raportów miesięcznych : {len(weekly_reports)}')

        # connecting all reports into one list
        reports_to_export = []
        reports_to_export.extend(daily_reports)
        reports_to_export.extend(weekly_reports)
        reports_to_export.extend(monthly_reports)

        # exporting list of queries to excel
        if reports_to_export:
            logger.info(f'shcedule: create_reports_on_schedule łączna ilość raportów: {len(reports_to_export)}')
            for raport in reports_to_export:
                if raport:
                    logger.info(f'shcedule: create_reports_on_schedule  tworzenie raportu: {raport.id}')
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
                    duration = end_time - start_time
                    raport.creation_time = datetime.datetime.strptime(str(datetime.timedelta(
                        seconds=round(duration))), "%H:%M:%S")
                    raport.last_creation = datetime.datetime.now()
                    db.session.commit()

    except Exception as err:
        logger.error(
            f'shcedule: create_reports_on_schedule wygenerował bład: {err}')


scheduler.add_job(id='s1',
                  name='reports_to_xlsx',
                  func=create_reports_on_schedule,
                  trigger='cron',
                  day_of_week='mon-sun',
                  hour=report_on_schedule_time.hour,
                  minute=report_on_schedule_time.minute,
                  timezone='Europe/Warsaw',
                  misfire_grace_time=5000)
scheduler.start()

class SchedulerConfig(FlaskForm):
    schedule_time = TimeField('Godzina generowania raportów')
    schedule_run = BooleanField()


@zakupy_front_bp.route('/scheduler', methods=['POST', 'GET'])
@admin_required
def scheduler_config_page():
    global report_on_schedule_time
    raport = SchedulerConfig()
    if raport.validate_on_submit():
        scheduler.reschedule_job('s1', trigger='cron',
                            hour=raport.schedule_time.data.hour,
                            minute=raport.schedule_time.data.minute,
                            timezone='Europe/Warsaw',
                            misfire_grace_time=5000)
        sheduler_list = scheduler.get_jobs()
        report_on_schedule_time = raport.schedule_time.data
    else:
        raport.schedule_time.data = report_on_schedule_time
        sheduler_list = scheduler.get_jobs()
    return render_template('scheduler_config_page.html', raport=raport, list_of_shedules=sheduler_list)