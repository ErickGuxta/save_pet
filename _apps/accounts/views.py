# ============================================================
# O app accounts cuida:
#
#   - cadastro/login/logout de usuários;
#   - detalhe, edição e exclusão da própria conta;
#   - perfil do tutor.
# ============================================================

# ============================================================
# Imports
# ============================================================

# importando mensagens, autenticação e shortcuts do Django
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# importando forms e model de perfil do tutor
from _apps.accounts.forms import LoginForm, PerfilUsuarioForm, PublicUserForm
from _apps.accounts.models import Usuario


# ============================================================
# Redirecionamentos básicos
# ============================================================

@login_required
def dashboard(request):
    # por enquanto o painel inicial do usuário é a listagem de pets
    return redirect("pets:index")


@login_required
def index(request):
    # rota inicial do accounts redireciona para os detalhes da conta
    return redirect("accounts:detail")


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
            # salva o usuário, cria o perfil do tutor e já faz login
            user = form.save()
            Usuario.objects.get_or_create(user=user)
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


def logout_view(request):
    # encerra a sessão do usuário logado
    logout(request)
    return redirect("accounts:login")


# ============================================================
# Conta do tutor
# ============================================================

@login_required
def detail(request):
    # garante que todo usuário tenha um perfil de tutor associado
    perfil, _ = Usuario.objects.get_or_create(user=request.user)

    context = {
        "perfil": perfil,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def edit(request):
    # carrega os dados atuais do usuário e perfil no formulário
    Usuario.objects.get_or_create(user=request.user)
    form = PerfilUsuarioForm(user=request.user)

    if request.method == "POST":
        # atualiza dados básicos do usuário e do perfil do tutor
        form = PerfilUsuarioForm(request.POST, user=request.user)

        if form.is_valid():
            user = request.user
            perfil = user.perfil

            user.first_name = form.cleaned_data["nome"]
            user.email = form.cleaned_data["email"]
            user.save()

            perfil.cpf = form.cleaned_data["cpf"] or None
            perfil.telefone = form.cleaned_data["telefone"]
            perfil.cep = form.cleaned_data["cep"]
            perfil.logradouro = form.cleaned_data["logradouro"]
            perfil.numero = form.cleaned_data["numero"]
            perfil.complemento = form.cleaned_data["complemento"]
            perfil.bairro = form.cleaned_data["bairro"]
            perfil.cidade = form.cleaned_data["cidade"]
            perfil.estado = form.cleaned_data["estado"]
            perfil.save()

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
