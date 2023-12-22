import requests
from bs4 import BeautifulSoup
import datetime
import mysql.connector
import json
import os
from collections import namedtuple
from types import SimpleNamespace

TotalRequests = 0
ValidRequests = 0
FailedRequests = 0
ExclusiveIPHits = 0
Refferers = 0
NotFound = 0
InitProcTime = 0
StaticFiles = 0
UniqueVisitors = 0
LogSize = 0
RequestedFiles = 0
TxAmount = 0
# variaveis que serão somadas.

def selectSQL():
    connection = mysql.connector.connect(
    host="localhost",
    user="FATEC",
    password="serverEaD",
    database="jsonparsed"
    ) # uma função que usa um dicionário como argumento

    cursor = connection.cursor()
    #codigoSQL = "SELECT * from json" # pega todos os valores, não precisa selecionar nenhum específico
    codigoSQL = "SELECT Json FROM json where IDJson > 0;" # pega os primeiros valores do json(para testes)

    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    #print("O resultado é de tipo " + str(type(resultado)))
    #resultado = str(resultado)
    # Precisamos tirar os parênteses que vem junto com o fetchall.
    # O jeito é dar append em cada valor da lista que o fetchall retorna numa nova lista.
    resultadosJson = []
    #contador = 0
    for json in resultado:
        #json = list(json) # já que strings são imutaveis, torna a string numa lista.
        #json[0] = ''
        #json[-1] = ''
        #printeiro = json[0]
        #print("Versão lista do json " + str(printeiro))
        # tira os parenteses.
        #json = str(json)
        #json = ''.join(json)
        #print("O json é de tipo " + str(type(json)))
        #print("O json é de tipo " + str(type(json[0])))
        resultadosJson.append(json[0]) # Coloco o valor json da lista resultado na lista resultadosJson
        # é uma copia real do valor da tupla, o str() retorna um valor diferente.
        # a razão disso é o fato que o json[0] é um typecasting, forçando a tupla a se tornar string.
        # O str(json) cria uma nova string baseada no valor do json, criando possivelmente sujeira e afins.
        # O método json.loads só aceita strings puras por completo. Logo typecasting funciona melhor
        # O jeito é forçar a variável a mudar, não simplesmente mudar ela ao que parece, Tenha uma ótima existencia. 
    #print("print dos resultados sem parenteses do select no final ficou: " + str(resultadosJson))
    cursor.close()
    connection.close()

    return resultadosJson
    

def printvariaveis():
    print("As variaveis somadas ficaram como: \n", 
          "\nTotal Requests:",TotalRequests, 
          "\nValid Requests:",ValidRequests, 
          "\nFailedRequests:",FailedRequests, 
          "\nExclusivePHits:",ExclusiveIPHits,
          "\nRefferers:",Refferers, 
          "\nNotfound:", NotFound, 
          "\nInitProcTime:", InitProcTime, 
          "\nStaticFIles:",StaticFiles, 
          "\nUniqueVisitors:", UniqueVisitors, 
          "\nLogsize:", LogSize, 
          "\nRequestedFiles:", RequestedFiles, 
          "\nTxAmount:", TxAmount)

def somaValores(objeto):
    # indicamos as variaveis globais
    global TotalRequests
    global ValidRequests
    global FailedRequests
    global ExclusiveIPHits
    global Refferers
    global NotFound
    global InitProcTime
    global StaticFiles
    global UniqueVisitors
    global LogSize
    global RequestedFiles
    global TxAmount
    #print("O total requests tem valor de: " + str(objeto.general.total_requests))
    #print("Variavel global aleatória: " + str(TotalRequests))
    print("Essa é a soma do resto com o dia: ", objeto.general.date_time)
    TotalRequests = TotalRequests + objeto.general.total_requests
    ValidRequests = ValidRequests + objeto.general.valid_requests
    print("O tipo do valid requests é: ", type(objeto.general.valid_requests))
    FailedRequests = FailedRequests + objeto.general.failed_requests
    ExclusiveIPHits = ExclusiveIPHits + objeto.general.unique_visitors
    Refferers = Refferers + objeto.general.unique_referrers
    NotFound = NotFound + objeto.general.unique_not_found
    InitProcTime = InitProcTime + objeto.general.generation_time
    StaticFiles = StaticFiles + objeto.general.unique_static_files
    UniqueVisitors = UniqueVisitors + objeto.general.unique_visitors
    LogSize = LogSize + objeto.general.log_size
    RequestedFiles = RequestedFiles + objeto.general.unique_files
    TxAmount = TxAmount + objeto.general.bandwidth
    printvariaveis()
    

# agora tenho que somar as variáveis do unico objeto criado através do unico json da lista de jsons do SQL.

    #soma = 0
    #print("A variavei de dicionario que chegou é " + dicionario + " " + dicionario2)
    #print("A variavel que iremos somar inicia em: " + str(json[dicionario][dicionario2]))
    #print("O dicionário é do tipo " + str(type(json)) + "E seu index: " + str(type(json[dicionario][dicionario2])))
    #print("O tamanho do dicionario é: " + str(len(json)))
    #for valor in json[dicionario][dicionario2]:
        #print(valor)


def listarAtributos(objeto): # função que imprime os atributos do objeto
    atributos = dir(objeto)
    for atributo in atributos:
        valor = getattr(objeto, atributo)
        print(f"{atributo}: {valor}")
        if isinstance(valor, dict):
            listarAtributos(valor)

def transformaObjeto(dicionario): # Poderia ser feito com SimpleNamespace
    for chave, valor in dicionario.items():
        if isinstance(valor, dict): # testa se o valor é um dicionário dentro de um dicionario.
            dicionario[chave] = transformaObjeto(valor) # Função recursiva, ela lança o valor do dicionário
            # e com esse valor, verifica se os valores dentro dele são dicionarios também.
            # depois de verifica-los, retorna um objeto que vai se adicionando.
    return namedtuple("Objeto", dicionario.keys())(**dicionario) # retorna um objeto com as keys do dicionario
    # que tem os valores de dicionario. Vai ser feito varias vezes e se somando até criar o objeto final.
    # O truque é que cada dicionário que ele descobriu, vai ter suas respectivas keys adicionadas e valores
    # adicionados no objeto no final.

#########################################################################################################

print("Iniciando decodificação e soma das variaveis do json.")
print("As variáveis que iremos somar são: Total requests, Valid Requests Failed Requests, Excl. IP Hits, refferers,")
print("Not found, Init Proc. Time, Unique visitors, Requested files, Static Files, Log size, Tx. Amount")
# esses dicionários se escrevem com _ e sem letras maiusculas.

selectSQL()
resultado = selectSQL() # pega as tuplas json do SQL
contador = 0
for valor in (resultado): # cada resultado da iteração, um novo objeto é formado.
    #contador += 1
    #print("batata " + str(contador))
    #print("O valor retornado foi: ")
    #print(valor)]
    #print(valor)
    contador = contador + 1
    try:
        jsonDecod = json.loads(str(valor))
        #print(str(jsonDecod))
        if (type(jsonDecod) != dict):
            continue
    except:
        print("O valor não pôde ser decodificado.")
    #print("Agora que o Json foi decodificado, vamos somar as variáveis.")
    #print("O json decod é de tipo:" + type(jsonDecod))
    #print(jsonDecod['general']['failed_requests']) # ou print(jsonDecod.get('visitors')) lembrar que variaveis estão
    # dentro de outras variaveis. Requests estão dentro de general.
    objeto = transformaObjeto(jsonDecod) # cria um unico objeto através de um unico json decodificado de um unico json
    #objeto = SimpleNamespace(**jsonDecod)
    #print(objeto.general._fields)
    #print("O dicionário virou objeto: " + str(objeto.general.start_date))
    #print("Vamos listar os atributos:")
    #listarAtributos(objeto)
    print("Entrou em soma valores, o loop é de posição:", contador)
    somaValores(objeto)
#printvariaveis()


###################################################
    # Nome do arquivo que você está procurando
    #nome_arquivo = 'ArquivoJsonTeste'
    # Caminho completo para o arquivo
    #caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    #with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        #jsonDecod = json.load(arquivo)
        #print(jsonDecod)

# O arquivo está corretamente formatado, o problema é o () do fetchall.
###################################################


###################################################
    # O problema é que isso não pega keys nested, só as superficiais.
    # Objeto = namedtuple("objeto", dicionario.keys())
    # objeto = Objeto(**dicionario)
###################################################