from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Categoria(models.Model):
    nome      = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    slug      = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name        = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ArtigoBlog(models.Model):
    STATUS_RASCUNHO = "rascunho"
    STATUS_PUBLICADO = "publicado"

    STATUS_CHOICES = [
        (STATUS_RASCUNHO, "Rascunho"),
        (STATUS_PUBLICADO, "Publicado"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,

        on_delete    =models.CASCADE,
        related_name ="artigos_blog",
    )
    categoria = models.ForeignKey(
        Categoria,

        on_delete    =models.PROTECT,
        related_name ="artigos",
    )

    titulo           = models.CharField(max_length=180)
    slug             = models.SlugField(max_length=210, unique=True, blank=True)
    resumo           = models.TextField(blank=True)
    conteudo         = models.TextField()
    imagem_url       = models.URLField("URL da imagem", blank=True)
    tempo_leitura    = models.PositiveIntegerField("Tempo de leitura em minutos", default=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PUBLICADO)
    data_publicacao  = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artigo do Blog"
        verbose_name_plural = "Artigos do Blog"
        ordering = ["-data_publicacao"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
