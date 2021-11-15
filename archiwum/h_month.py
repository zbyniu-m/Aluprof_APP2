import pandas as pd
import cx_Oracle
import sqlite3
from datetime import datetime, timedelta
import time
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# config definitions for oracle connections
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
cx_Oracle.init_oracle_client(lib_dir=r"C:\\instatntclient\\instantclient_19_12")
load_dotenv(env_file)

# config definitions for logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('logs_h_month.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

cx_con = cx_Oracle.connect(user=os.environ.get('CX_LOGIN'), password=os.environ.get('CX_PASSWORD'),
                           dsn=os.environ.get('CX_DNS'), encoding="UTF-8")


# function definitions for sqlite connections
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        logger.error(
            f'Harmonogram: create_connection_sqlite, Bład: {e}')
    return conn


def update_query_table(conn, task):
    sqlite_update = ''' UPDATE query_table 
                    SET 
                    creation_time=?,
                    last_creation=? 
                    WHERE id=?
                    '''
    cur = conn.cursor()
    cur.execute(sqlite_update, task)
    conn.commit()


def select_data_from_query_table(sqlite_con) -> list:
    sqlite_query = """
    select query_name, localization, query_string, id from query_table where schedule = true and schedule_interval = 'm'
    """
    cursor = sqlite_con.cursor()
    cursor.execute(sqlite_query)
    sqlite_list = cursor.fetchall()
    cursor.close()
    return sqlite_list


# config definitions for sqlite
sqlite_db = 'aluprof_app/database.db'
sqlite_con = create_connection(sqlite_db)


# Beginning of algorithm
sqlite_list = select_data_from_query_table(sqlite_con)
if sqlite_list:
    for raport in sqlite_list:
        try:
            if raport[2]:
                start_time = time.time()
                lokalizacja = raport[1]
                if not os.path.exists(lokalizacja):
                    os.makedirs(lokalizacja)
                    logger.info(f'utworzono katalog {lokalizacja}')
                queries = raport[2].split(";")
                df = []

                # preparing list of dataframe from list of queries
                for query in queries:
                    if query:
                        query = query.strip()
                        df.append(pd.read_sql_query(query, cx_con))
                path = os.path.join(raport[1], raport[0].strip().replace(' ', '_') + '.xlsx')
                writer = pd.ExcelWriter(path, engine='xlsxwriter')
                numerator = 0

                # Saving dataframe to Excel
                for data in df:
                    sheet_name = raport[0].strip().replace(' ', '_')
                    if len(sheet_name) > 20:
                        sheet_name = sheet_name[:20] + str(numerator)
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

                    numerator = +1
                writer.save()
                end_time = time.time()

                # Saving parameters to database
                duration = end_time - start_time
                creation_time = datetime.strptime(str(timedelta(seconds=round(duration))), "%H:%M:%S")
                last_creation = datetime.now()
                logger.info(f'Harmonogram: tworzenie raportu {raport[0]} zakończono sukcesem')
                with sqlite_con:
                    update_query_table(sqlite_con, (creation_time, last_creation, raport[3]))

        except Exception as err:
            logger.error(
                f'Harmonogram: tworzenie raportu o {raport[0]}, Bład: {err}')
else:
    logger.info(f'Harmonogram: brak raportów do utworzenia.')
