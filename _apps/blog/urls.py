from django.urls import path

from . import views


app_name = "blog"

urlpatterns = [
    path("",                  views.articles, name="index"),
    path("create/",           views.create,   name="create"),
    path("<int:id>/",         views.detail,   name="detail"),
    path("<int:id>/edit/",    views.edit,     name="edit"),
    path("<int:id>/delete/",  views.delete,   name="delete"),

    path("categories/",                 views.categories,      name="categories"),
    path("categories/create/",          views.category_create, name="category_create"),
    path("categories/<int:id>/edit/",   views.category_edit,   name="category_edit"),
    path("categories/<int:id>/delete/", views.category_delete, name="category_delete"),
]
