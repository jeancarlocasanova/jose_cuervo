import datetime
import os
import django
from django.core.wsgi import get_wsgi_application
from django.conf import settings
import jose_cuervo.settings
from django.core.wsgi import get_wsgi_application
import pyodbc

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "f2candon.settings")
application = get_wsgi_application()
django.setup()

def main_engine():
    db_config = settings.DATABASES['default']

    # Establece la cadena de conexión
    connection_string = (
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={db_config['HOST']};"
        f"DATABASE={db_config['NAME']};"
        f"UID={db_config['USER']};"
        f"PWD={db_config['PASSWORD']};"
    )
    # Conecta a la base de datos
    conn = pyodbc.connect(connection_string)

    # Crea un cursor
    cursor = conn.cursor()
    while True:
        queryHistorian = """SELECT * FROM HistorianRawData where Processed = -1"""
        cursor.execute(queryHistorian)
        rows = cursor.fetchall()
        labels_scanned = [{"date": row[0], "line": row[1], "url": row[3]} for row in rows]

main_engine()
