"""
URL configuration for servidor_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

#teste/batata corta o primeiro teste e manda o batata, ele vê o inicio e deixa o app teste.urls lidar com resto
# cada path leva a um servidor django de nome tal.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("teste/", include ("teste.urls")) # toda url teste vai para as urls do app teste
]
