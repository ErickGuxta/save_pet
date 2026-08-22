from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    TIPO_TUTOR         = "tutor"
    TIPO_ADMINISTRADOR = "administrador"

    TIPO_CHOICES = [
        (TIPO_TUTOR, "Tutor"),
        (TIPO_ADMINISTRADOR, "Administrador"),
    ]

    user        = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    cpf         = models.CharField("CPF", max_length=14, unique=True, blank=True, null=True)
    telefone    = models.CharField("telefone", max_length=20, blank=True)
    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_TUTOR)
    cep         = models.CharField("CEP", max_length=9, blank=True)
    logradouro  = models.CharField(max_length=150, blank=True)
    numero      = models.CharField(max_length=20,  blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro      = models.CharField(max_length=100, blank=True)
    cidade      = models.CharField(max_length=100, blank=True)
    estado      = models.CharField(max_length=2,   blank=True)

    class Meta:
        verbose_name        = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.user.get_full_name() or self.user.username