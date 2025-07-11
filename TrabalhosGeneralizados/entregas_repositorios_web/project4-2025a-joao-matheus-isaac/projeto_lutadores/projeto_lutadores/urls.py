"""
URL configuration for projeto_lutadores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include # Include não incluido


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_lutadores.urls')), # Exemplo de app principal, redirecionamento automatico, já que a URL sempre vem "vazia" ''
    #path('nome_do_app', include('nome_do_app.urls')), # Exemplo de redirecionamento usando uma URL para acesso às outras URLS
]

