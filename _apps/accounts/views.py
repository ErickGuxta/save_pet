# ============================================================
# O app accounts cuida:
#
#   - cadastro/login/logout de usuários;
#   - detalhe, edição e exclusão da própria conta;
#   - dados cadastrais do tutor.
# ============================================================

# ============================================================
# Imports
# ============================================================

# importando mensagens, autenticação e shortcuts do Django
from django.contrib                 import messages
from django.contrib.auth            import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models     import Group, User
from django.utils                   import timezone
from django.views.decorators.http   import require_POST
from django.shortcuts               import redirect, render

# importando forms de autenticação e cadastro
from _apps.accounts.forms  import LoginForm, PerfilDonoForm, PublicUserForm
from _apps.accounts.models import Dono
from _apps.blog.models     import ArtigoBlog, Categoria
from _apps.pets.models     import Pet
from _apps.vaccines.models import RegistroVacina


BLOG_EDITOR_GROUP_NAME = "Editor do blog"


def is_admin_sistema(user):
    return user.is_authenticated and user.has_perm("auth.change_user")


# ============================================================
# Redirecionamentos básicos
# ============================================================

@login_required
def dashboard(request):
    if is_admin_sistema(request.user):
        total_donos = sum(
            1 for dono in Dono.objects.select_related("user_ptr")
            if not is_admin_sistema(dono)
        )
        context = {
            "total_users": User.objects.count(),
            "total_donos": total_donos,
            "total_pets": Pet.objects.count(),
            "total_vaccines": RegistroVacina.objects.count(),
            "total_articles": ArtigoBlog.objects.count(),
            "total_categories": Categoria.objects.count(),
            "recent_pets": Pet.objects.select_related("dono").order_by("-data_atualizacao_saude")[:5],
            "recent_articles": ArtigoBlog.objects.select_related("categoria", "dono").order_by("-data_publicacao")[:5],
        }
        return render(request, "accounts/admin_dashboard.html", context)

    dono = Dono.objects.filter(pk=request.user.pk).first()
    if dono is None:
        messages.error(request, "Seu usuário não possui perfil de tutor.")
        return redirect("blog:index")

    pets = Pet.objects.filter(dono=dono)
    context = {
        "total_pets": pets.count(),
        "total_vaccines": RegistroVacina.objects.filter(pet__dono=dono).count(),
        "pets": pets.order_by("nome")[:6],
        "upcoming_vaccines": RegistroVacina.objects.filter(
            pet__dono=dono,
            data_reforco__isnull=False,
            data_reforco__gte=timezone.localdate(),
        ).select_related("pet").order_by("data_reforco")[:5],
        "recent_articles": ArtigoBlog.objects.select_related("categoria", "dono").order_by("-data_publicacao")[:3],
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def index(request):
    # rota inicial do accounts redireciona para os detalhes da conta
    return redirect("accounts:detail")


@login_required
@permission_required("auth.change_user", raise_exception=True)
def users_permissions(request):
    editor_group = Group.objects.filter(name=BLOG_EDITOR_GROUP_NAME).first()
    if editor_group is None:
        messages.error(request, "Crie o grupo Editor do blog no painel admin do Django.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role_action = request.POST.get("role_action")
        user = User.objects.filter(pk=user_id).first()

        if user is None:
            messages.error(request, "Usuário não encontrado.")
            return redirect("accounts:users_permissions")

        if user.is_staff or user.is_superuser or is_admin_sistema(user):
            messages.error(request, "Contas administrativas devem ser gerenciadas pelo painel admin do Django.")
            return redirect("accounts:users_permissions")

        if role_action == "add_editor":
            user.groups.add(editor_group)
            messages.success(request, f"{user.username} agora é editor do blog.")
            return redirect("accounts:users_permissions")

        if role_action == "remove_editor":
            user.groups.remove(editor_group)
            messages.success(request, f"{user.username} não é mais editor do blog.")
            return redirect("accounts:users_permissions")

        messages.error(request, "Ação inválida.")
        return redirect("accounts:users_permissions")

    users = []
    for user in User.objects.prefetch_related("groups").order_by("username"):
        is_app_admin = is_admin_sistema(user)
        users.append({
            "user": user,
            "is_app_admin": is_app_admin,
            "is_blog_editor": user.groups.filter(pk=editor_group.pk).exists(),
            "can_edit_blog_role": not user.is_staff and not user.is_superuser and not is_app_admin,
        })

    context = {
        "users": users,
        "admin_group_name": BLOG_EDITOR_GROUP_NAME,
    }
    return render(request, "accounts/users_permissions.html", context)


# ============================================================
# Cadastro público de tutor
# ============================================================

def create(request):
    # instanciando o formulário de cadastro público
    form = PublicUserForm()

    if request.method == "POST":
        # recebendo os dados enviados pelo formulário
        form = PublicUserForm(request.POST)

        if form.is_valid():
            # salva o tutor e já faz login
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("pets:index")

    context = {
        "form": form,
    }
    return render(request, "accounts/create.html", context)


# ============================================================
# Login e logout
# ============================================================

def login_view(request):
    # formulário padrão de autenticação do Django com bootstrap no forms.py
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        # se usuário e senha estiverem corretos, autentica e redireciona
        login(request, form.get_user())
        return redirect("pets:index")

    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@require_POST
def logout_view(request):
    # encerra a sessão do usuário logado
    logout(request)
    return redirect("accounts:login")


# ============================================================
# Conta do tutor
# ============================================================

@login_required
def detail(request):
    dono = Dono.objects.filter(pk=request.user.pk).first()
    context = {
        "dono": dono,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def edit(request):
    # carrega os dados atuais do usuário no formulário
    dono = Dono.objects.filter(pk=request.user.pk).first()
    form = PerfilDonoForm(user=request.user, dono=dono)

    if request.method == "POST":
        # atualiza dados básicos e cadastrais do tutor
        form = PerfilDonoForm(request.POST, user=request.user, dono=dono)

        if form.is_valid():
            user = request.user

            user.first_name      = form.cleaned_data["nome"]
            user.email           = form.cleaned_data["email"]
            user.save()

            if dono is not None:
                dono.cpf             = form.cleaned_data["cpf"] or None
                dono.telefone        = form.cleaned_data["telefone"]
                dono.cep             = form.cleaned_data["cep"]
                dono.logradouro      = form.cleaned_data["logradouro"]
                dono.numero          = form.cleaned_data["numero"]
                dono.complemento     = form.cleaned_data["complemento"]
                dono.bairro          = form.cleaned_data["bairro"]
                dono.cidade          = form.cleaned_data["cidade"]
                dono.estado          = form.cleaned_data["estado"]
                dono.save()

            messages.success(request, "Conta atualizada.")
            return redirect("accounts:detail")

    context = {
        "form": form,
    }
    return render(request, "accounts/edit.html", context)


@login_required
def delete(request):
    # exclui a própria conta somente quando o formulário for confirmado
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Conta excluída com sucesso.")
        return redirect("accounts:login")

    return render(request, "accounts/delete.html")
