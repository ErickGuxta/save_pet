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
from django.contrib.auth.decorators import login_required

# importando formulário e model de vacinas
from .forms  import VaccineForm
from .models import RegistroVacina


# ============================================================
# Vacinas
# ============================================================

# Listar registros de vacinas
@login_required
def vaccines(request):
    # lista apenas as vacinas do usuário logado
    vaccines = RegistroVacina.objects.filter(
        pet__usuario=request.user
    ).select_related("pet")

    context = {
        "vaccines": vaccines,
    }

    return render(request, "vaccines/index.html", context)


# Detalhar vacina
@login_required
def detail(request, id):
    # busca a vacina pelo ID e garante que pertence ao usuário logado
    vaccine = get_object_or_404(
        RegistroVacina,
        id=id,
        pet__usuario=request.user,
    )

    context = {
        "vaccine": vaccine
    }

    return render(request, "vaccines/detail.html", context)


# Criar registro de vacina
@login_required
def create(request):
    # instanciando a metaclasse VaccineForm filtrando pets do usuário logado
    form = VaccineForm(user=request.user)

    if request.method == "POST":
        # recebendo os dados enviados pelo formulário
        form = VaccineForm(request.POST, user=request.user)

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
def edit(request, id):

    # busca a vacina que será editada
    vaccine = get_object_or_404(
        RegistroVacina,
        id=id,
        pet__usuario=request.user,
    )
    form = VaccineForm(instance=vaccine, user=request.user)

    if request.method == "POST":
        # atualiza a vacina com os dados enviados no formulário
        form = VaccineForm(request.POST, instance=vaccine, user=request.user)

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
def delete(request, id):
    # busca e exclui a vacina informada na URL
    vaccine = get_object_or_404(
        RegistroVacina,
        id=id,
        pet__usuario=request.user,
    )
    vaccine.delete()
    messages.success(request, "Vacina excluída com sucesso.")
    return redirect("vaccines:index")
