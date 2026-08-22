"""
URL configuration for save_pet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/'           , admin.site.urls),

   # path(''                 , views.dashboard, name="dashboard"),
    path('access/'          , include("django.contrib.auth.urls")),

    # path('painel-admin/'    , include("_apps.adminpanel.urls")),
    # path('users/'           , include("_apps.accounts.urls")),
    # path('pets/'            , include("_apps.pets.urls")),
    # path('vaccines/'        , include("_apps.vaccines.urls")),
    # path('locator/'         , include("_apps.locator.urls")),
    # path('blog/'            , include("_apps.blog.urls")),
]
