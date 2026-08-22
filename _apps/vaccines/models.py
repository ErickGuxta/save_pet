from django.db import models
from django.contrib.auth.models import User

from _apps.pets.models import Pet

# Create your models here.
class Vaccine(models.Model):
    nome                = models.CharField(max_length=100)
    lote                = models.CharField(max_length=50)
    data_aplicacao      = models.DateField()
    data_reforco        = models.DateField(blank=True, null=True)
    veterinario         = models.CharField(max_length=100)
    clinica             = models.CharField(max_length=100)
    observacoes         = models.TextField(blank=True)

    pet                 = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE, 
        related_name="vacinas"
        )

    usuario             = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="vacinas"
        )

    class Meta:
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"
    
    def __str__(self):
        return self.nome
