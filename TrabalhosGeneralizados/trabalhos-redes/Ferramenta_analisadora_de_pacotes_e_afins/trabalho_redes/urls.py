from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('meu_aplicativo/', include('meu_aplicativo.urls')),
    path('index/', index, name = 'index'),
    path('', charts_view, name = 'charts')
    # Outras rotas do projeto aqui...
]
