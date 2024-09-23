from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bairro(models.Model):
    bairro = models.CharField(max_length=100)

    def __str__(self):
        return self.bairro



class Casa(models.Model):
    valor = models.PositiveBigIntegerField(null=True)
    quartos = models.PositiveSmallIntegerField(null=True)
    area = models.DecimalField(max_digits=11,decimal_places=2,null=True)
    endereco = models.CharField(max_length=100)
    nome_bairro = models.ForeignKey(Bairro,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"endereço: {self.endereco} | id: {self.id}"
    




