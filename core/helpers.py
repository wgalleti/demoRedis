import cx_Oracle
from django.db import connections
from django.utils import timezone
from rest_framework.exceptions import ParseError


def custom_query(query, filter=[], str_con='gatec'):
    """
    Returno custom query (SQLRaw)
    :param query: SQL Instruction
    :param filter: Filter to Apply (Array)
    :param str_con: String database connection
    :return: Dict
    """
    with connections[str_con].cursor() as cursor:
        cursor.execute(query, filter)
        columns = [col[0].lower() for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for i in enumerate(data):
            for c in columns:
                if type(data[i[0]][c]) == cx_Oracle.LOB:
                    data[i[0]][c] = data[i[0]][c].read()

                if type(data[i[0]][c]) == cx_Oracle.DATETIME:
                    data[i[0]][c] = timezone.make_aware(data[i[0]][c], timezone.get_current_timezone())

        return data


def _checkRequired(action, *args, **kwargs):
    data = dict()
    filter = False
    if action in ['list', 'custom']:
        filter = True
        for a in args:
            data[a] = kwargs.get(a, None)
            if data[a] is None:
                raise ParseError(detail=f'Filtro {a} é obrigatório', code=400)

            if type(data[a]) == list:
                data[a] = data[a][0]
    return data, filter
