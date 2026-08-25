from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from _apps.accounts.models import Dono


@admin.register(Dono)
class DonoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados do dono",
            {
                "fields": (
                    "cpf",
                    "telefone",
                    "cep",
                    "logradouro",
                    "numero",
                    "complemento",
                    "bairro",
                    "cidade",
                    "estado",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dados do dono",
            {
                "fields": (
                    "cpf",
                    "telefone",
                    "cep",
                    "logradouro",
                    "numero",
                    "complemento",
                    "bairro",
                    "cidade",
                    "estado",
                )
            },
        ),
    )
