from django.contrib import admin
from django.urls import include, path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('remover/<int:id_lutador>/', remover_lutador, name='remover_lutador'),
    path('criar_lutador/', criar_lutador_view, name='criar_lutador'),
    path('lutador/<int:id_lutador>/', ver_lutador_view, name='ver_lutador'),
    path('editar_lutador/<int:id_lutador>/', editar_lutador_view, name='editar_lutador'),
    path('adicionar_golpe/', adicionar_golpe_view, name='adicionar_golpe'),
    path('golpes/', lista_golpes_view, name='lista_golpes'),
    path('golpe/<int:id_golpe>/', ver_golpe_view, name='ver_golpe'),
    path('editar_golpe/<int:id_golpe>/', editar_golpe_view, name='editar_golpe'),
    path('remover_golpe/<int:id_golpe>/', remover_golpe_view, name='remover_golpe'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('criar_lutador/', criar_lutador_view, name='criar_lutador'),
    path('exemplo/', exemplo_view, name='exemplo'),  
]