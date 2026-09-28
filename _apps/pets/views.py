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
from django.views.decorators.http import require_POST

# importando formulário e model de pets
from .forms import PetForm
from .models import Pet
from _apps.accounts.models import Dono
from _apps.accounts.permissions import is_admin_sistema



# ============================================================
# Pets
# ============================================================

# Listar pets
@login_required
def pets(request):
    # admin vê todos; tutor comum vê apenas os próprios pets
    if is_admin_sistema(request.user):
        pets = Pet.objects.all()
    else:
        dono = get_object_or_404(Dono, pk=request.user.pk)
        pets = Pet.objects.filter(dono=dono)

    context = {
        "pets": pets,
    }

    return render(request, "pets/index.html", context)

# Detalhar pet
@login_required
def detail(request, id):
    # admin pode abrir qualquer pet; tutor comum apenas os próprios
    pets_query = Pet.objects.prefetch_related("vacinas")
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        pets_query = pets_query.filter(dono=dono)

    pet = get_object_or_404(pets_query, id=id)

    context = {
        "pet": pet,

    }

    return render(request, "pets/detail.html", context)

# Criar pet
@login_required
def create(request):
    # instanciando a metaclasse PetForm
    dono = Dono.objects.filter(pk=request.user.pk).first()
    if dono is None:
        messages.error(request, "Para cadastrar pet, entre com uma conta de tutor.")
        return redirect("pets:index")

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
    pets_query = Pet.objects.all()
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        pets_query = pets_query.filter(dono=dono)

    pet = get_object_or_404(pets_query, id=id)
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
@require_POST
def delete(request, id):
    # busca e exclui o pet informado na URL
    pets_query = Pet.objects.all()
    if not is_admin_sistema(request.user):
        dono = get_object_or_404(Dono, pk=request.user.pk)
        pets_query = pets_query.filter(dono=dono)

    pet = get_object_or_404(pets_query, id=id)
    pet.delete()
    messages.success(request, "Pet excluído com sucesso.")
    return redirect("pets:index")
