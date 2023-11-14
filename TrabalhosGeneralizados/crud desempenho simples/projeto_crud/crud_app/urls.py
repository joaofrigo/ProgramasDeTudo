# meu_projeto/projeto_crud/urls.py
from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='nome_da_url_home'),
    # ... outras URLs do seu aplicativo ...
]
