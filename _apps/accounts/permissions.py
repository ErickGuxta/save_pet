ADMIN_GROUP_NAME = "Administrador do sistema"


def is_admin_sistema(user):
    if not user.is_authenticated:
        return False

    return (
        user.is_staff
        or user.is_superuser
        or user.groups.filter(name=ADMIN_GROUP_NAME).exists()
    )


def admin_context(request):
    return {
        "is_admin_sistema": is_admin_sistema(request.user),
    }
