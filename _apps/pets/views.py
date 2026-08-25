# ============================================================
# O app pets cuida:
#
#   - cadastro de pets;
#   - listagem de pets do tutor logado;
#   - edição, detalhe e exclusão de pets.
# ============================================================

# ============================================================
# Imports
# ============================================================

# importando shortcuts para renderização, busca e redirecionamento
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# importando formulário e model de pets
from .forms import PetForm
from .models import Pet
from _apps.accounts.models import Dono



# ============================================================
# Pets
# ============================================================

# Listar pets
@login_required
def pets(request):
    # lista apenas os pets do usuário logado
    dono = get_object_or_404(Dono, pk=request.user.pk)
    pets = Pet.objects.filter(dono=dono)

    context = {
        "pets": pets,
    }

    return render(request, "pets/index.html", context)

# Detalhar pet
@login_required
def detail(request, id):
    # busca o pet pelo ID e garante que pertence ao usuário logado
    dono = get_object_or_404(Dono, pk=request.user.pk)
    pet = get_object_or_404(
        Pet.objects.prefetch_related("vacinas"),
        id=id,
        dono=dono,
    )

    context = {
        "pet": pet,

    }

    return render(request, "pets/detail.html", context)

# Criar pet
@login_required
def create(request):
    # instanciando a metaclasse PetForm
    dono = get_object_or_404(Dono, pk=request.user.pk)
    form = PetForm()

    if request.method == "POST":
        # recebendo os dados enviados pelo formulário
        form = PetForm(request.POST, request.FILES)

        if form.is_valid():
            # salva o pet com vínculo ao usuário logado
            pet = form.save(commit=False)
            pet.dono = dono

            pet.save()
            messages.success(request, "Pet cadastrado com sucesso.")
            return redirect("pets:index")
        # se não for válido renderiza a tela de criar novamente
        else:
            context = {
                "form": form
            }
            return render(request, "pets/create.html", context)

    context = {
        "form": form
    }

    return render(request, "pets/create.html", context)

# Editar pet
@login_required
def edit(request, id):

    # busca o pet que será editado
    dono = get_object_or_404(Dono, pk=request.user.pk)
    pet = get_object_or_404(Pet, id=id, dono=dono)
    form = PetForm(instance=pet)

    if request.method == "POST":
        # atualiza o pet com os dados enviados no formulário
        form = PetForm(request.POST, request.FILES, instance=pet)

        if form.is_valid():
            form.save()
            messages.success(request, "Pet atualizado com sucesso.")
            return redirect("pets:index")
        else:
            context = {
                "form": form
            }
            return render(request, "pets/edit.html", context)

    context = {
        "form": form
    }

    return render(request, "pets/edit.html", context)


# Excluir pet
@login_required
def delete(request, id):
    # busca e exclui o pet informado na URL
    dono = get_object_or_404(Dono, pk=request.user.pk)
    pet = get_object_or_404(Pet, id=id, dono=dono)
    pet.delete()
    messages.success(request, "Pet excluído com sucesso.")
    return redirect("pets:index")
