from django.db import models
from django.contrib.auth.models import User


class Dono(User):
    cpf         = models.CharField("CPF", max_length=14, unique=True, blank=True, null=True)
    telefone    = models.CharField("telefone", max_length=20, blank=True)
    cep         = models.CharField("CEP", max_length=9, blank=True)
    logradouro  = models.CharField(max_length=150, blank=True)
    numero      = models.CharField(max_length=20,  blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro      = models.CharField(max_length=100, blank=True)
    cidade      = models.CharField(max_length=100, blank=True)
    estado      = models.CharField(max_length=2,   blank=True)

    class Meta:
        verbose_name        = "dono"
        verbose_name_plural = "donos"

    def __str__(self):
        return self.get_full_name() or self.username
