from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '_apps.accounts'

    def ready(self):
        import _apps.accounts.signals
