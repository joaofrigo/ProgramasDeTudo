import requests
from bs4 import BeautifulSoup
import datetime
import mysql.connector
import json
import requests
from types import SimpleNamespace
import time

def insereSQL(conteudo, URL, objetoJson, cursor):

    datetimeInserir = str(objetoJson.general.date_time).replace(" -0300", "")
    codigoSQL = "INSERT INTO json (json, url, data) VALUES (%s, %s, %s);"
    #print("O datetime que será isnerido é: ", datetimeInserir)
    informacao = (conteudo, URL, datetimeInserir) # o valor do json URL e do datetime

    cursor.execute(codigoSQL, informacao)


def transformaObjeto(dicionario):
    objeto = SimpleNamespace()  # Cria um objeto vazio usando SimpleNamespace, esse objeto é especial por ser
    # bem mais dinamico que o namedtuple. Seus atributos são dinâmicos, por isso aceitam novos valores no futuro
    # diferentemente de namedtuple. Namedtuple é bom para leitura porém, por ser imutável.
    for chave, valor in dicionario.items():
        if isinstance(valor, dict):  # Verifica se o valor é um dicionário
            setattr(objeto, chave, transformaObjeto(valor))  # Atribui um objeto aninhado, no caso vai mais
            # fundo na aninhação do dicionário chamando a si mesmo com o novo valor. Assim o valor desse atributo
            # ao invés de ser um dicionário, é o objeto desse dicionário, por causa do return.
        else:
            setattr(objeto, chave, valor)  # Atribui o valor diretamente ao atributo, já que não é um dicionário.
            # o for vai percorrer todas as chaves do dicionário e todos os valores relacionados a essa chave.
            # o for no caso percorre o dicionário de aninhamento atual.

    return objeto


def inserirOuNao(conteudo, cursor):

    datetimeExiste = conteudo.general.date_time
    datetimeExiste = str(datetimeExiste.replace(" -0300", ""))
    #datetimeExiste = datetime(datetimeExiste)
    codigoSQL = "SELECT id FROM json WHERE data = %s"
    informacao = (datetimeExiste,) # o valor do datetime que vai ser pesquisado na tabela
    #print("A informação que procuramos é ", informacao)

    cursor.execute(codigoSQL, informacao) # Só preciso dar execute não commit. Commit só se alterou algo.
    resultado = cursor.fetchall()
    #print("O tipo do resultado que recebi do inserir ou não é: ", type(resultado), 
    #      "Com os valores de: ", resultado)

    valoresLista = len(resultado)
    if valoresLista >= 1: # Se existe algo nessa lista, no caso retornou alguma data igual.
        valorID = str(resultado[0])
        valorID = valorID.replace(",", "")
        print("O resultado que está sendo retornado é de ID ", valorID)
        return valorID # não deve inserir, deve modificar essa data.
    else: 
        return 0 # não existe, deve inserir


def converteTempoString(dia):
    dia = str(dia) # transforma em string
    dia = dia.split("-") # tira os traços
    dia = ''.join(dia) # concatena os valores. soma '' mais um valor da lista e reitera.
    return dia

def modificaSQL(conteudo, idInserir, cursor):
    #print ("O arquivo de json de detetime ", datetimeInserir, "Será modificado")
    #f"Olá, {nome}! Você tem {idade} anos."
    #conteudo = '{"unicornio": 1}'
    #data_dict = json.loads(conteudo)
    # Transformar dicionário em tupla
    #data_tuple = tuple(data_dict.items())

    #datetimeInserir = '2020-04-21 13:04:49'
    #codigoSQL = f"update json set json = JSON_OBJECT{conteudo} where data = '{datetimeInserir}'" # coloco o novo json onde se encontra o valor
    #codigoSQL = "update json set json = JSON_OBJECT'conteudo' where data = 'datetimeInserir'"
    codigoSQL = "update json set json = %s where id = %s"
    #codigoSQL = "UPDATE json SET json = '{}' WHERE data = {}".format(conteudo, datetimeInserir)
    # de data repetido (recebido da função anterior)
    informacao = (conteudo, idInserir) # o valor que vai modificar e onde modificar
    #print("A string do codigo SQL ficou:\n",codigoSQL)
    
    cursor.execute(codigoSQL, informacao)

    #print("Foi modificado o valor de data ", datetimeInserir, "Com Sucesso")


################################################################################### funcao principal
def iniciar():
    dia = datetime.date(2020, 1, 9) # o inicio dos tempos.
    diaFinal = datetime.date.today() # o dia hipotético final.
    tempoSoma = datetime.timedelta(days= 1)
    numeroFalhas = 0
    Excepetion = 0
    tempoInicio = 0
    tempoFinal = 0

    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma única conexão para governar todas
    cursor = connection.cursor() # o cursor rei

    while dia < diaFinal:
        diaString = converteTempoString(dia)
        URL = "exemplo.com/" + diaString + ".html"
        request = requests.get(url = URL)
        conteudo = 0 # inicializar fora para evitar problemas de falta de inicialização
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, "lxml")
            VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
            try:
                conteudo = VarJson[1].text # Pega o que tem dentro da tag.
                conteudo = conteudo.replace("var json_data=", "") # Tira o "var json_data=" e deixa só as chaves.
                # Colocar o if se existe antes do insereSQL, se não existe dá insere, se existe modifica.
                if (conteudo != 0):
                    tempoInicio = time.time()
                    counteudoAuxiliar = json.loads(conteudo) # vai levar o json para virar objeto
                    counteudoAuxiliar = transformaObjeto(counteudoAuxiliar) # transforma dicionario em objeto
                    tempoFinal = time.time()
                    tempo = tempoFinal - tempoInicio
                    print("O tempo total usado para manipulação do json é: ", tempo)
                    tempoInicio = time.time()
                    print("O json atual está com o tipo de: ", type(counteudoAuxiliar))
                    inserir = inserirOuNao(counteudoAuxiliar, cursor) # pega esse objeto e vê se o datetime dele existe no SQL.
                    tempoFinal = time.time()
                    tempo = tempoFinal - tempoInicio
                    print("O tempo total usado para o inserir ou não é ", tempo)
                    # Continuar a inserção do if da data se existe
                if (inserir == 0):
                    tempoInicio = time.time()
                    insereSQL(conteudo, URL, counteudoAuxiliar, cursor)
                    tempoFinal = time.time()
                    tempo = tempoFinal - tempoInicio
                    print("O tempo total usado para a inserção no SQL é", tempo)
                    print ("Conteudo de datetime ", str(counteudoAuxiliar.general.date_time).replace(" -0300", ""), " foi inserido")
                else:
                    tempoInicio = time.time()
                    modificaSQL(conteudo, inserir, cursor)
                    tempoFinal = time.time()
                    tempo = tempoFinal - tempoInicio
                    print("O tempo total usado para modificar o valor no SQL é", tempo)
                    print ("Conteudo de ID ", inserir, " foi modificado")

            #except Excepetion as e:        
            except:
                conteudo = None
                numeroFalhas += 1
                #print("A exceção é essa: ", Excepetion)
                print("Erro na formatação do htmtl, os valores do dia " + diaString + " não serão inseridos.")
                print("Ou é erro no SQL.")
        else:
            print("O status/resposta do request que no dia " + diaString + " deu erro, é: " + str(request.status_code))  # dá 404 quando não achar, só fazer assim para verificar as datas inexistentes.
        
        
        
        #if (conteudo != 0):
        #    counteudoAuxiliar = json.loads(conteudo) # vai levar o json para virar objeto
        #   counteudoAuxiliar = transformaObjeto(counteudoAuxiliar) # transforma dicionario em objeto
        #    inserir = inserirOuNao(counteudoAuxiliar) # pega esse objeto e vê se o datetime dele existe no SQL.
        #    # Continuar a inserção do if da data se existe
        #    if (inserir == 0):
        #        print ("Conteudo de datetime ", counteudoAuxiliar.general.date_time, " será inserido")
        #        insereSQL(conteudo, URL, counteudoAuxiliar)
        #   else:
        #        print ("Conteudo de datetime ", counteudoAuxiliar.general.date_time, " será modificado")
            #modificaSQL(conteudo, URL, counteudoAuxiliar)
        dia = dia + tempoSoma # para parar o while, soma os dias (objetos dia)
    print("Ocorreram " + str(numeroFalhas) + " falhas")
    connection.commit()
    cursor.close()
    connection.close()

"""
def selectSQL(): # Pega um json da lista e retorna
    connection = mysql.connector.connect(
    host="localhost",
    user="FATEC",
    password="serverEaD",
    database="jsonparsed"
    )

    cursor = connection.cursor()
    #codigoSQL = "SELECT * from json" # pega todos os valores, não precisa selecionar nenhum específico
    codigoSQL = "SELECT Json FROM json where IDJson > 0;" # pega os primeiros valores do json(para testes)

    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    resultadosJson = []
    for json in resultado:
        resultadosJson.append(json[0]) # Coloco o valor json da lista resultado na lista resultadosJson
    cursor.close()
    connection.close()

    return resultadosJson
"""


# Agora trocar e retornar o iD ao invés do datetime, quando se encontra um datetime igual.
# Fazer isso para fazer o where com o ID ao invés do datetime a comparação, mais rápido daí

iniciar()