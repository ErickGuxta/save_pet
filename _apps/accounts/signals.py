from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from _apps.accounts.permissions import ADMIN_GROUP_NAME


@receiver(post_migrate)
def criar_grupo_admin_sistema(sender, **kwargs):
    if sender.label != "accounts":
        return

    group, _ = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
    permissions = Permission.objects.all()
    group.permissions.add(*permissions)
