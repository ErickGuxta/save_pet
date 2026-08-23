from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import PetForm
from .models import Pet


#Listar pets
def pets(request):
    pets = Pet.objects.filter(usuario=request.user)

    context = {
        "pets": pets,
    }

    return render(request, "pets/index.html", context)

def detail(request, id):
    pet = get_object_or_404(
        Pet.objects.prefetch_related("vacinas").select_related("rastreador"),
        id=id,
        usuario=request.user,
    )

    context = {
        "pet": pet,

    }

    return render(request, "pets/detail.html", context)

#Criar Pet
def create(request):
    form = PetForm()

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)

        if form.is_valid():
            pet = form.save(commit=False)
            pet.usuario = request.user

            pet.save()
            messages.success(request, "Pet cadastrado com sucesso.")
            return redirect("pets:index")
        #se não for válido renderiza a tela de criar novamente
        else:
            context = {
                "form": form
            }
            return render(request, "pets/create.html", context)

    context = {
        "form": form
    }

    return render(request, "pets/create.html", context)

#Editar Pet
def edit(request, id):

    pet = get_object_or_404(Pet, id=id, usuario=request.user)
    form = PetForm(instance=pet)

    if request.method == "POST":
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


#Excluir Pet
def delete(request, id):
    pet = get_object_or_404(Pet, id=id, usuario=request.user)
    pet.delete()
    messages.success(request, "Pet excluído com sucesso.")
    return redirect("pets:index")