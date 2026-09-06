from django.contrib                 import messages
from django.contrib.auth.decorators import login_required
from django.db.models.deletion      import ProtectedError
from django.shortcuts               import get_object_or_404, redirect, render

from _apps.accounts.models import Dono

from .forms  import ArtigoBlogForm, CategoriaForm
from .models import ArtigoBlog, Categoria


@login_required
def articles(request):
    dono = get_object_or_404(Dono, pk=request.user.pk)
    articles = ArtigoBlog.objects.filter(dono=dono).select_related("categoria")

    return render(request, "blog/index.html", {"articles": articles})


@login_required
def detail(request, id):
    dono = get_object_or_404(Dono, pk=request.user.pk)
    article = get_object_or_404(
        ArtigoBlog.objects.select_related("categoria"),
        id=id,
        dono=dono,
    )

    return render(request, "blog/detail.html", {"article": article})


@login_required
def create(request):
    dono = get_object_or_404(Dono, pk=request.user.pk)
    form = ArtigoBlogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.dono = dono
        article.save()
        messages.success(request, "Artigo cadastrado com sucesso.")
        return redirect("blog:index")

    return render(request, "blog/create.html", {"form": form})


@login_required
def edit(request, id):
    dono = get_object_or_404(Dono, pk=request.user.pk)
    article = get_object_or_404(ArtigoBlog, id=id, dono=dono)
    form = ArtigoBlogForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artigo atualizado com sucesso.")
        return redirect("blog:index")

    return render(request, "blog/edit.html", {"form": form, "article": article})


@login_required
def delete(request, id):
    dono = get_object_or_404(Dono, pk=request.user.pk)
    article = get_object_or_404(ArtigoBlog, id=id, dono=dono)
    article.delete()
    messages.success(request, "Artigo excluído com sucesso.")
    return redirect("blog:index")


@login_required
def categories(request):
    return render(
        request,
        "blog/categories.html",
        {"categories": Categoria.objects.all()},
    )


@login_required
def category_create(request):
    form = CategoriaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoria cadastrada com sucesso.")
        return redirect("blog:categories")

    return render(request, "blog/category_form.html", {"form": form, "title": "Nova categoria"})


@login_required
def category_edit(request, id):
    category = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoria atualizada com sucesso.")
        return redirect("blog:categories")

    return render(request, "blog/category_form.html", {"form": form, "title": "Editar categoria"})


@login_required
def category_delete(request, id):
    category = get_object_or_404(Categoria, id=id)

    try:
        category.delete()
        messages.success(request, "Categoria excluída com sucesso.")
    except ProtectedError:
        messages.error(request, "A categoria possui artigos e não pode ser excluída.")

    return redirect("blog:categories")
