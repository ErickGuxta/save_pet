from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("",           views.index,       name="index"),
    path("dashboard/", views.dashboard,   name="dashboard"),
    path("create/",    views.create,      name="create"),

    path("login/",     views.login_view,  name="login"),
    path("logout/",    views.logout_view, name="logout"),
    path("profile/",   views.detail,      name="profile"),
    
    path("detail/",    views.detail,      name="detail"),
    path("edit/",      views.edit,        name="edit"),
    path("delete/",    views.delete,      name="delete"),
]
