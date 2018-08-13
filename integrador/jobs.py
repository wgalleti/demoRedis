from django_rq import job

from integrador.models import Empresa, Safra
from integrador.queries import IntegradorQueries


class IntegradorJob:

    def __init__(self):
        self.de_para = [dict(query='empresa', model=Empresa),
                        dict(query='safra', model=Safra)]
        self.query = IntegradorQueries()

    def run(self):
        for i in self.de_para:
            print(self.query.receber(**i))


@job('high')
def go():
    a = IntegradorJob()
    a.run()


go.delay()
