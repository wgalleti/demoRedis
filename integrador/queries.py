from core.helpers import custom_query
from django.utils import timezone
from core.models import Consulta

EMPRESA = """
SELECT COD_EMPR AS ID,
       INITCAP(TRIM(ABV_EMPR)) AS NOME
  FROM GA_EMPR
 ORDER BY 1  
"""

SAFRA = """
SELECT COD_EMPR || COD_SAFRA AS ID,
       COD_EMPR AS EMPRESA_ID,
       COD_SAFRA AS NOME,
       SAF_ANO_SAFRA AS ANO
  FROM GA_SAF_SAFRAS
 ORDER BY 2, 4, 3
"""


class IntegradorQueries:

    def __init__(self):
        self.query = dict()
        self.query['empresa'] = EMPRESA
        self.query['safra'] = SAFRA

    def receber_todos(self):
        result = dict()

        for q in self.query:
            result[q] = self.receber(query=self.query[q])

        return result

    def receber(self, **kwargs):
        query = kwargs.get('query', None)
        filters = kwargs.get('filters', [])
        data = []
        consulta = dict()
        consulta['sql'] = query
        consulta['parametros'] = ','.join(str(x) for x in filters)

        if query is None:
            return data

        consulta['inicio'] = timezone.now()
        try:
            data = custom_query(self.query[query], filters)
            consulta['termino'] = timezone.now()
            consulta['resultado'] = f'Retornou {len(data)} registros'
        except Exception as e:
            consulta['erro'] = True
            consulta['resultado'] = e[0:99]

        Consulta(**consulta).save()

        return data
