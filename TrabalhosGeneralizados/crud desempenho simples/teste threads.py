from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time 

def insercao_escrita_desempenho(cursor, conexao):
    # Implemente a lógica da inserção aqui
    print("Inserção realizada\n")

def select_leitura_desempenho(cursor):
    # Implemente a lógica da seleção aqui
    print("Seleção realizada\n")

# Número total de clientes
clientes = 50

# Criando funções parciais com os argumentos fixos
insercao_parcial = partial(insercao_escrita_desempenho, 3, 4)
select_parcial = partial(select_leitura_desempenho, 3)

# Lista de funções parciais
funcoes_parciais = [insercao_parcial] * (clientes // 2) + [select_parcial] * (clientes // 2)

temporizador_inicial = time.time()

with ThreadPoolExecutor(max_workers=clientes) as executor:
    # Usando executor.submit para cada função parcial
    futures = [executor.submit(funcao) for funcao in funcoes_parciais]

    # Aguardando a conclusão das chamadas
    for future in futures:
        future.result()

temporizador_final = time.time()
tempo_decorrido = temporizador_final - temporizador_inicial
print("O tempo decorrido foi de:", tempo_decorrido)
