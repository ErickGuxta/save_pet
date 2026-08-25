from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Pet(models.Model):
    nome                = models.CharField(max_length=100)
    
    especie             = models.CharField(max_length=50, choices=[
        ("Cachorro", "Cachorro"),
        ("Gato", "Gato"),       
        ("Pássaro", "Pássaro"),
        ("Roedor", "Roedor"),
        ("Outro", "Outro"),
    ])
    sexo                = models.CharField(max_length=10, choices=[
        ("Macho", "Macho"),
        ("Fêmea", "Fêmea"),
    ])
    
    raca                = models.CharField(max_length=50)
    data_nascimento     = models.DateField()
    pelagem             = models.CharField(max_length=50)
    peso                = models.FloatField()
    foto                = models.ImageField(upload_to="pets/fotos/", blank=True, null=True)
    alergias            = models.TextField(blank=True)
    doencas             = models.TextField(blank=True)
    medicamentos        = models.TextField(blank=True)
    observacoes         = models.TextField(blank=True)

    usuario             = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="pets"
        )

    data_atualizacao_saude = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
    

    def __str__(self):
        return self.nome
