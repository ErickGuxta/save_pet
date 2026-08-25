from django.db import models
from django.utils import timezone
from _apps.accounts.models import Dono



class Categoria(models.Model):
    nome      = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name        = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class ArtigoBlog(models.Model):
    dono = models.ForeignKey(
        Dono,
        on_delete    =models.CASCADE,
        related_name ="artigos_blog",
    )
    categoria = models.ForeignKey(
        Categoria,

        on_delete    =models.PROTECT,
        related_name ="artigos",
    )

    titulo           = models.CharField(max_length=180)
    conteudo         = models.TextField()
    
    data_publicacao  = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artigo do Blog"
        verbose_name_plural = "Artigos do Blog"
        ordering = ["-data_publicacao"]

    def __str__(self):
        return self.titulo
