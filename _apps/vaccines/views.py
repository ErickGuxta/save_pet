from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms  import VaccineForm
from .models import Vaccine


#Listar Registros de Vacinas
def vaccines(request):
    vaccines = Vaccine.objects.filter(usuario=request.user).select_related("pet")

    context = {
        "vaccines": vaccines,
    }

    return render(request, "vaccines/index.html", context)


def detail(request, id):
    vaccine = get_object_or_404(Vaccine, id=id, usuario=request.user)

    context = {
        "vaccine": vaccine
    }

    return render(request, "vaccines/detail.html", context)


#Criar Registro Vacina
def create(request):
    form = VaccineForm(user=request.user)

    if request.method == "POST":
        form = VaccineForm(request.POST, user=request.user)

        if form.is_valid():
            vaccine = form.save(commit=False)
            vaccine.usuario = request.user

            vaccine.save()
            messages.success(request, "Vacina cadastrada com sucesso.")
            return redirect("vaccines:index")
        #se não for válido renderiza a tela de criar novamente
        else:
            context = {
                "form": form
            }
            return render(request, "vaccines/create.html", context)

    context = {
        "form": form
    }

    return render(request, "vaccines/create.html", context)


#Editar Registro vacina
def edit(request, id):

    vaccine = get_object_or_404(Vaccine, id=id, usuario=request.user)
    form = VaccineForm(instance=vaccine, user=request.user)

    if request.method == "POST":
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



#Excluir Registro vacina
def delete(request, id):
    vaccine = get_object_or_404(Vaccine, id=id, usuario=request.user)
    vaccine.delete()
    messages.success(request, "Vacina excluída com sucesso.")
    return redirect("vaccines:index")