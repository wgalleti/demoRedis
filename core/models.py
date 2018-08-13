from django.db import models


class Consulta(models.Model):
    inicio = models.DateTimeField()
    sql = models.TextField()
    parametros = models.TextField()
    termino = models.DateTimeField()
    resultado = models.CharField(max_length=100)
    erro = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}'


class Erro(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('auth.User', null=True, blank=True)
    log = models.TextField()
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
