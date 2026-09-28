from django.contrib                 import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.deletion      import ProtectedError
from django.shortcuts               import get_object_or_404, redirect, render
from django.views.decorators.http   import require_POST

from _apps.accounts.models import Dono
from _apps.accounts.permissions import is_admin_sistema

from .forms  import ArtigoBlogForm, CategoriaForm
from .models import ArtigoBlog,     Categoria


admin_required = user_passes_test(is_admin_sistema, login_url="/blog/")


def dono_do_admin(user):
    dono, _ = Dono.objects.update_or_create(
        user_ptr_id=user.pk,
        defaults={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
        },
    )
    return dono


@login_required
def articles(request):
    # Dono/tutor apenas visualiza; admin visualiza e gerencia.
    articles = ArtigoBlog.objects.select_related("categoria")

    return render(request, "blog/index.html", {"articles": articles})


@login_required
def detail(request, id):
    articles_query = ArtigoBlog.objects.select_related("categoria")
    article = get_object_or_404(articles_query, id=id)

    return render(request, "blog/detail.html", {"article": article})


@login_required
@admin_required
def create(request):
    form = ArtigoBlogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.dono = dono_do_admin(request.user)
        article.save()
        messages.success(request, "Artigo cadastrado com sucesso.")
        return redirect("blog:index")

    return render(request, "blog/create.html", {"form": form})


@login_required
@admin_required
def edit(request, id):
    article = get_object_or_404(ArtigoBlog, id=id)
    form = ArtigoBlogForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artigo atualizado com sucesso.")
        return redirect("blog:index")

    return render(request, "blog/edit.html", {"form": form, "article": article})


@login_required
@admin_required
@require_POST
def delete(request, id):
    article = get_object_or_404(ArtigoBlog, id=id)
    article.delete()
    messages.success(request, "Artigo excluído com sucesso.")
    return redirect("blog:index")


@login_required
@admin_required
def categories(request):
    return render(
        request,
        "blog/categories.html",
        {"categories": Categoria.objects.all()},
    )


@login_required
@admin_required
def category_create(request):
    form = CategoriaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoria cadastrada com sucesso.")
        return redirect("blog:categories")

    return render(request, "blog/category_form.html", {"form": form, "title": "Nova categoria"})


@login_required
@admin_required
def category_edit(request, id):
    category = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoria atualizada com sucesso.")
        return redirect("blog:categories")

    return render(request, "blog/category_form.html", {"form": form, "title": "Editar categoria"})


@login_required
@admin_required
@require_POST
def category_delete(request, id):
    category = get_object_or_404(Categoria, id=id)

    try:
        category.delete()
        messages.success(request, "Categoria excluída com sucesso.")
    except ProtectedError:
        messages.error(request, "A categoria possui artigos e não pode ser excluída.")

    return redirect("blog:categories")
