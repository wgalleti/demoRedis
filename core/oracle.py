import datetime

import cx_Oracle
from decouple import config
from dj_database_url import parse
from django.utils import timezone


class Database:

    def __init__(self, auto_connect=True):
        dbenv = config('DB_GATEC', cast=parse)

        self.host = dbenv['HOST']
        self.port = dbenv['PORT']
        self.service = dbenv['NAME']
        self.user = dbenv['USER']
        self.pwd = dbenv['PASSWORD']
        self.connection = None

        if auto_connect:
            self.open(rac=True)

    def tns(self):
        self.tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)

    def open(self, rac=False):
        self.tns()
        try:
            self.connection = cx_Oracle.connect(self.user, self.pwd, self.tns, threaded=rac)
        except cx_Oracle.DatabaseError as e:
            self.connection = None
            print(e)

    def disconnect(self):
        self.connection.close()

    def query(self, sql, filters=[], parse_tz=False):
        if 'select' not in sql.lower():
            print('Comando SQL inválido!')
            return []

        cursor = self.connection.cursor()
        cursor.execute(sql, filters)
        columns = [col[0].lower() for col in cursor.description]

        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        for i in enumerate(data):
            for c in columns:
                if type(data[i[0]][c]) == cx_Oracle.LOB:
                    data[i[0]][c] = data[i[0]][c].read()
                if type(data[i[0]][c]) == datetime.datetime and parse_tz:
                    data[i[0]][c] = timezone.make_aware(data[i[0]][c], timezone.get_current_timezone())

        return data

    def update(self, sql, data={}, commit=True):
        if 'update' not in sql.lower():
            print('Comando SQL inválido!')
            return {}

        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, data)
            if commit:
                self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            self.error = f'{e}'
            return False

        return True
