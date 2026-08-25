from django.db import models
from _apps.pets.models import Pet

# Create your models here.
class RegistroVacina(models.Model):
    nome_vacina          = models.CharField(max_length=100)
    lote                = models.CharField(max_length=50)
    data_aplicacao      = models.DateField()
    data_reforco        = models.DateField(blank=True, null=True)
    veterinario         = models.CharField(max_length=100)
    clinica             = models.CharField(max_length=100)
    observacoes         = models.CharField(max_length=255, blank=True)

    pet                 = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE, 
        related_name="vacinas"
        )

    class Meta:
        verbose_name = "Registro de vacina"
        verbose_name_plural = "Registros de vacina"
    
    def __str__(self):
        return self.nome_vacina
