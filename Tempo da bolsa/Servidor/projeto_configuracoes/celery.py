# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Defina o padrão para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_configuracoes.settings')

# Crie uma instância do Celery
app = Celery('Meu_projeto')

# Carregue configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregue tarefas de todos os aplicativos Django
app.autodiscover_tasks()
