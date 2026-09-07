from django.contrib import admin

from .models import ArtigoBlog
from .models import Categoria

admin.site.register(ArtigoBlog)
admin.site.register(Categoria)
