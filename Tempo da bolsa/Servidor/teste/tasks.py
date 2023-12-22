from celery import Celery
from celery import shared_task
from subprocess import run

app = Celery('teste')

@shared_task
def executar_script_inicial():
    print("vou executar le script")
    run(["python", "/home/joao/Downloads/Pasta gitbucket/Servidor/teste/script_inicial.py"])


#executar_script_inicial()
