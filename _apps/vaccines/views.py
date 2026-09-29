# ============================================================
# O app vaccines cuida:
#
#   - cadastro de vacinas;
#   - listagem de vacinas do tutor logado;
#   - edição, detalhe e exclusão de vacinas.
# ============================================================

# ============================================================
# Imports
# ============================================================

# importando shortcuts para renderização, busca e redirecionamento
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

# importando formulário e model de vacinas
from .forms  import VaccineForm
from .models import RegistroVacina
from _apps.accounts.models import Dono


def is_admin_sistema(user):
    return user.is_authenticated and user.has_perm("auth.change_user")



# ============================================================
# Vacinas
# ============================================================

# Listar registros de vacinas
@login_required
@permission_required("vaccines.view_registrovacina", raise_exception=True)
def vaccines(request):
    # admin vê todas; tutor comum vê apenas as próprias vacinas
    vaccines = RegistroVacina.objects.select_related("pet")
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        vaccines = vaccines.filter(pet__dono=dono)

    context = {
        "vaccines": vaccines,
    }

    return render(request, "vaccines/index.html", context)


# Detalhar vacina
@login_required
@permission_required("vaccines.view_registrovacina", raise_exception=True)
def detail(request, id):
    # admin pode abrir qualquer vacina; tutor comum apenas as próprias
    vaccines_query = RegistroVacina.objects.all()
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        vaccines_query = vaccines_query.filter(pet__dono=dono)

    vaccine = get_object_or_404(vaccines_query, id=id)

    context = {
        "vaccine": vaccine
    }

    return render(request, "vaccines/detail.html", context)


# Criar registro de vacina
@login_required
@permission_required("vaccines.add_registrovacina", raise_exception=True)
def create(request):
    # instanciando a metaclasse VaccineForm filtrando pets do usuário logado
    dono = None
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)

    form = VaccineForm(dono=dono)

    if request.method == "POST":
        # recebendo os dados enviados pelo formulário
        form = VaccineForm(request.POST, dono=dono)

        if form.is_valid():
            # salva a vacina com vínculo ao usuário logado
            form.save()
            messages.success(request, "Vacina cadastrada com sucesso.")
            return redirect("vaccines:index")
        # se não for válido renderiza a tela de criar novamente
        else:
            context = {
                "form": form
            }
            return render(request, "vaccines/create.html", context)

    context = {
        "form": form
    }

    return render(request, "vaccines/create.html", context)


# Editar registro de vacina
@login_required
@permission_required("vaccines.change_registrovacina", raise_exception=True)
def edit(request, id):

    # busca a vacina que será editada
    dono = None
    vaccines_query = RegistroVacina.objects.all()
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        vaccines_query = vaccines_query.filter(pet__dono=dono)

    vaccine = get_object_or_404(vaccines_query, id=id)
    form = VaccineForm(instance=vaccine, dono=dono)

    if request.method == "POST":
        # atualiza a vacina com os dados enviados no formulário
        form = VaccineForm(request.POST, instance=vaccine, dono=dono)

        if form.is_valid():
            form.save()
            messages.success(request, "Vacina atualizada com sucesso.")
            return redirect("vaccines:index")
        else:
            context = {
                "form": form
            }
            return render(request, "vaccines/edit.html", context)

    context = {
        "form": form
    }

    return render(request, "vaccines/edit.html", context)



# Excluir registro de vacina
@login_required
@permission_required("vaccines.delete_registrovacina", raise_exception=True)
@require_POST
def delete(request, id):
    # busca e exclui a vacina informada na URL
    vaccines_query = RegistroVacina.objects.all()
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        vaccines_query = vaccines_query.filter(pet__dono=dono)

    vaccine = get_object_or_404(vaccines_query, id=id)
    vaccine.delete()
    messages.success(request, "Vacina excluída com sucesso.")
    return redirect("vaccines:index")
