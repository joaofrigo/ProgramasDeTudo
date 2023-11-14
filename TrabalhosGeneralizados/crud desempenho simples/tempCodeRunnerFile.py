import threading
import time

def funcao1():
    print("Função 1\n")
    time.sleep(1)
    print("Função 1 terminou\n")

def funcao2():
    print("Função 2\n")
    time.sleep(1)
    print("Função 2 terminou\n")

def executor_de_funcoes(lista_de_funcoes):
    threads = []
    for funcao, quantidade in lista_de_funcoes:
        for _ in range(quantidade):
            thread = threading.Thread(target=funcao)
            threads.append(thread)

    # Inicia todas as threads
    for thread in threads:
        thread.start()

    # Aguarda o término de todas as threads
    for thread in threads:
        thread.join()

# Exemplo de uso
lista_de_funcoes = [(funcao1, 25), (funcao2, 25)]

executor_de_funcoes(lista_de_funcoes)
