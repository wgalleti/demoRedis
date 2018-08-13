from django.db import models


class Empresa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Safra(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    empresa = models.ForeignKey('integrador.Empresa', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    ano = models.IntegerField()

    def __str__(self):
        return self.nome
