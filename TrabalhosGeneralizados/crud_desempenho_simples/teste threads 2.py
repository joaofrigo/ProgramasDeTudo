from functools import partial
import threading
import time

def insercao_escrita_desempenho(cursor, conexao):
    # Simulando uma operação de inserção
    time.sleep(1)
    print("Inserção realizada\n")

def select_leitura_desempenho(cursor, conexao):
    # Simulando uma operação de seleção
    time.sleep(1)
    print("Seleção realizada\n")

def executor_de_funcoes(lista_de_funcoes):
    threads = []
    for funcao in lista_de_funcoes:
        thread = threading.Thread(target=funcao)
        threads.append(thread)

    # Inicia todas as threads
    for thread in threads:
        thread.start()

    # Aguarda o término de todas as threads
    for thread in threads:
        thread.join()

# Exemplo de uso
cursor = "Exemplo de cursor"
conexao = "Exemplo de conexão"

# Criando 25 funções parciais de inserção e 25 de seleção
funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(25)]
funcoes_selecao = [partial(select_leitura_desempenho, cursor, conexao) for _ in range(25)]

# Adicionando as funções à lista de funções
lista_de_funcoes = funcoes_insercao + funcoes_selecao

executor_de_funcoes(lista_de_funcoes)
