import mysql.connector
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time
import sys
import threading

def transforma_em_id(ID):
    # Utiliza zfill para encher de 0 (especificação da base de dados)
    #print("O ID é: ", ID)
    string_padrao = "tt"
    numero_id = str(ID).zfill(7)
    id_real = string_padrao + numero_id
    #print("O ID ficou como:", id_real)
    return str(id_real)

def desfaz_em_numero(ID):
    #print("O ID bobo é:", ID[0])
    ID = str(ID[0])
    ID = ID.replace("tt", "")
    #print("O ID em formato numero é:", int(ID))
    return int(ID)

def insercao(cursor):
    #print("Inserindo valor de ID novo. Não ocupará o espaço de algum ID antigo se deletado anteriormente, contagem continua linear")
    media = input("Insira classificação média: ")
    votos = input("Insira quantos votos foram contabilizados: ")

    # Encontra o último valor
    codigoSQL = "SELECT id FROM movie_ratings ORDER BY id DESC LIMIT 1"
    cursor.execute(codigoSQL)
    ultimo_ID = cursor.fetchone()
    ultimo_ID = desfaz_em_numero(ultimo_ID)
    ultimo_ID = ultimo_ID + 1
    ID_final = transforma_em_id(ultimo_ID)

    codigoSQL = """
        INSERT INTO movie_ratings (id, averageRating, numVotes)
        VALUES (%s, %s, %s);
    """
    parametros = (ID_final, media, votos)

    print("O código antes de sua execução é:", codigoSQL)
    cursor.execute(codigoSQL, parametros)



def delete(cursor):
    print("Insira o ID do valor que quer remover.")
    ID = input()
    ID = transforma_em_id(ID)
    codigoSQL= """
        DELETE FROM movie_ratings
        WHERE id = %s
    """
    parametros = (ID,)
    cursor.execute(codigoSQL, parametros)


def update(cursor):
    print("Insira o ID que quer modificar")
    ID = input()
    ID = transforma_em_id(ID)
    print("Agora insira os novos valores para averageRating e numVotes:")
    averageRating = input()
    numVotes = input()
    codigoSQL = """
        UPDATE movie_ratings
        SET averageRating = %s, numVotes = %s
        WHERE id = %s;
    """
    parametros = (ID, averageRating, numVotes)
    cursor.execute(codigoSQL, parametros)

def select(cursor):
    print("Insira o ID que quer ler os dados")
    ID = input()
    ID = transforma_em_id(ID)
    codigoSQL = """
        SELECT * FROM movie_ratings
        WHERE id = %s;
    """
    parametros = (ID,)
    cursor.execute(codigoSQL,parametros)
    resultado = cursor.fetchall()
    print("Resultado da consulta select:", resultado)


def select_leitura_desempenho(cursor):
    conexao = mysql.connector.connect(
        user= "root",
        password= "1234",
        host= "localhost",
        database= "movies"
    ) # login feito através de um dicionario

    # Criar um objeto de cursor para executar consultas SQL
    cursor = conexao.cursor()
    
    ID = 1 # ID hipotético que será lido multiplas vezes por todos os clientes simultâneamente
    ID = transforma_em_id(ID)
    #print("Faremos o select\n")
    codigoSQL = """
        SELECT * FROM movie_ratings
        WHERE id = %s;
    """
    parametros = (ID,)
    cursor.execute(codigoSQL,parametros)
    #print("fizemos o select\n")
    resultado = cursor.fetchall() # sempre precisa existir para evitar erros de output
    #print("Resultado da consulta select:", resultado,"(Teste de desempenho)\n")
    #sys.stdout.flush()

def insercao_escrita_desempenho(cursor, conexao):
    #print("Inserindo valor de ID novo. Não ocupará o espaço de algum ID antigo se deletado anteriormente, contagem continua linear")
    conexao = mysql.connector.connect(
        user= "root",
        password= "1234",
        host= "localhost",
        database= "movies"
    ) # login feito através de um dicionario

    # Criar um objeto de cursor para executar consultas SQL
    cursor = conexao.cursor()
    media = 3.5
    votos = 40

    # Encontra o último valor
    codigoSQL = "SELECT id FROM movie_ratings ORDER BY id DESC LIMIT 1"
    cursor.execute(codigoSQL)
    ultimo_ID = cursor.fetchone()
    ultimo_ID = desfaz_em_numero(ultimo_ID)
    ultimo_ID = ultimo_ID + 1
    ID_final = transforma_em_id(ultimo_ID)

    codigoSQL = """
        INSERT INTO movie_ratings (id, averageRating, numVotes)
        VALUES (%s, %s, %s);
    """
    parametros = (ID_final, media, votos)
    cursor.execute(codigoSQL, parametros)
    conexao.commit()
    #sys.stdout.flush()


def executor_de_funcoes(lista_de_funcoes):
    threads = []
    for funcao in lista_de_funcoes: # Cria a lista de funções para a Thread (clientes)
        thread = threading.Thread(target=funcao)
        threads.append(thread)

    # Inicia todas as threads
    for thread in threads:
        thread.start()

    # Aguarda o término de todas as threads (clientes)
    for thread in threads:
        thread.join()

def teste_desempenho(cursor, conexao): # os commits são feitos em batchs de clientes. todos eles fazem e o commit é feito. Evita erros no BD.
    print("Iniciando teste de desempenho. Quantos clientes usarão o serviço simultaneamente?")
    clientes = int(input())
    print("Escolha a porcentagem de clientes que farão inserções ou leituras:")
    print("1 = 50 de leituras e 50 de escritas\n2 = 75 de leituras e 25 de escritas\n3 = 25 de leituras e 75 de escritas")
    escolha = int(input())
    if escolha == 1:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.50)
        clientes_escrita = round(clientes * 0.50)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 1 foi de:", tempo_decorrido)

    if escolha == 2:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.75)
        clientes_escrita = round(clientes * 0.25)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 2 foi de:", tempo_decorrido)

    if escolha == 3:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.75)
        clientes_escrita = round(clientes * 0.25)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 3 foi de:", tempo_decorrido)

def insercao_escrita_desempenho_pequeno(cursor, conexao):
    conexao = mysql.connector.connect(
        user= "root",
        password= "1234",
        host= "localhost",
        database= "movies"
    ) # login feito através de um dicionario

    # Criar um objeto de cursor para executar consultas SQL
    cursor = conexao.cursor()
    #print("Inserindo valor de ID novo. Não ocupará o espaço de algum ID antigo se deletado anteriormente, contagem continua linear")
    media = 999
    votos = 666

    # Encontra o último valor
    codigoSQL = "SELECT id FROM movie_ratings_pequeno ORDER BY id DESC LIMIT 1"
    cursor.execute(codigoSQL)
    ultimo_ID = cursor.fetchone()
    ultimo_ID = desfaz_em_numero(ultimo_ID)
    ultimo_ID = ultimo_ID + 1
    ID_final = transforma_em_id(ultimo_ID)

    codigoSQL = """
        INSERT INTO movie_ratings_pequeno (id, averageRating, numVotes)
        VALUES (%s, %s, %s);
    """
    parametros = (ID_final, media, votos)
    cursor.execute(codigoSQL, parametros)
    conexao.commit()

def select_leitura_desempenho_pequeno(cursor):
    conexao = mysql.connector.connect(
        user= "root",
        password= "1234",
        host= "localhost",
        database= "movies"
    ) # login feito através de um dicionario

    # Criar um objeto de cursor para executar consultas SQL
    cursor = conexao.cursor()
    ID = 1 # ID hipotético que será lido multiplas vezes por todos os clientes simultâneamente
    ID = transforma_em_id(ID)
    codigoSQL = """
        SELECT * FROM movie_ratings_pequeno
        WHERE id = %s;
    """
    parametros = (ID,)
    cursor.execute(codigoSQL,parametros)
    resultado = cursor.fetchall()  # sempre precisa existir para evitar erros de output
    #print("Resultado da consulta select:", resultado,"(Teste de desempenho)")

def teste_desempenho_pequeno(cursor, conexao):
    print("Iniciando teste de desempenho de database pequena. Quantos clientes usarão o serviço simultaneamente?")
    clientes = int(input())
    print("Escolha a porcentagem de clientes que farão inserções ou leituras:")
    print("1 = 50 de leituras e 50 de escritas\n2 = 75 de leituras e 25 de escritas\n3 = 25 de leituras e 75 de escritas")
    escolha = int(input())
    if escolha == 1:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.50)
        clientes_escrita = round(clientes * 0.50)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 1 foi de:", tempo_decorrido)

    if escolha == 2:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.75)
        clientes_escrita = round(clientes * 0.25)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 2 foi de:", tempo_decorrido)

    if escolha == 3:
        temporizador_inicial = time.time()
        clientes_leitura = round(clientes * 0.25)
        clientes_escrita = round(clientes * 0.75)
        # Criando funções parciais para enviar para as threads executarem
        funcoes_insercao = [partial(insercao_escrita_desempenho, cursor, conexao) for _ in range(clientes_escrita)]
        funcoes_selecao = [partial(select_leitura_desempenho, cursor) for _ in range(clientes_leitura)]
        # Adicionando as funções à lista de funções
        lista_de_funcoes = funcoes_insercao + funcoes_selecao
        executor_de_funcoes(lista_de_funcoes)
        temporizador_final = time.time()
        tempo_decorrido = temporizador_final - temporizador_inicial
        print("O tempo decorrido da escolha 3 foi de:", tempo_decorrido)

def operacoes_CRUD(cursor, conexao):
    while 1 == 1:
        print("Qual será sua próxima ação?")
        print("inserção = 1 \ndelete = 2 \nupdate = 3 \nselect = 4\nsair = 5\nrepetição com X clientes = 6\nrepetição com X clientes com database pequena = 7")
        acao = int(input()) # input é recebido sempre como string
        print("Sua ação é de valor:", acao)
        if acao == 1:
            insercao(cursor)
            print("Insert realizado")
        if acao == 2:
            delete(cursor)
            print("Delete realizado")
        if acao == 3:
            update(cursor)
            print("Update realizado")
        if acao == 4:
            select(cursor)
            print("Select finalizado")
        if acao == 5:
            return
        if acao == 6:
            teste_desempenho(cursor, conexao) # mandando a conexão para fazer commits a cada iteração para melhor teste
        if acao == 7:
            teste_desempenho_pequeno(cursor, conexao)


    #insercao() # insere um novo ultimo valor (se algo foi deletade anteriormente, ocupa esse espaço de ID)
    #delete() # deleta por ID
    #update() # update dos dois valores dentro desse ID
    #select() # seleciona um ID e retorna dados.

def main():
    # Criar uma conexão com o banco de dados
    conexao = mysql.connector.connect(
        user= "root",
        password= "1234",
        host= "localhost",
        database= "movies"
    ) # login feito através de um dicionario

    # Criar um objeto de cursor para executar consultas SQL
    cursor = conexao.cursor()
    operacoes_CRUD(cursor, conexao)
    # Fechar o cursor e a conexão
    print("Codigo será finalizado e commit final realizado")
    conexao.commit()
    cursor.close()
    conexao.close()


main()