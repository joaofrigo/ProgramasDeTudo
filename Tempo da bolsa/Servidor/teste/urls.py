from django.urls import path
from . import views

app_name ='teste'
#Configurações URL. Cada path leva a uma função do view. primeiro nome é como é chamado no site, 
# a segunda, o que ele chama
urlpatterns = [
    path("batata/", views.hello_world),
    path("dashboard_general/", views.dashboard_general, name = "dashboard_general"),
    path("hello_template/", views.hello_template),
    path("teste_html/", views.teste_html),
    path("homeDjango/", views.home_django),
    #path("dashboard_general_teste", views.dashboard_general_teste)
    #path("teste_html/links/exemplo_link.html/", views.outro_link)
]