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
    objeto = SimpleNamespace()
    for chave, valor in dicionario.items():
        if isinstance(valor, dict):  
            setattr(objeto, chave, transformaObjeto(valor))
        else:
            setattr(objeto, chave, valor) 

    return objeto


def inserirOuNao(conteudo, cursor):

    datetimeExiste = conteudo.general.date_time
    datetimeExiste = str(datetimeExiste.replace(" -0300", ""))
    codigoSQL = "SELECT id FROM json WHERE data = %s"
    informacao = (datetimeExiste,) # o valor do datetime que vai ser pesquisado na tabela

    cursor.execute(codigoSQL, informacao) # Só preciso dar execute não commit. Commit só se alterou algo.
    resultado = cursor.fetchall()

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
    codigoSQL = "update json set json = %s where id = %s"
    informacao = (conteudo, idInserir) # o valor que vai modificar e onde modificar
    cursor.execute(codigoSQL, informacao)

def iniciar():
    dia = datetime.date(2020, 1, 9) # o inicio dos tempos.
    diaFinal = datetime.date.today() # o dia hipotético final.
    tempoSoma = datetime.timedelta(days= 1)
    numeroFalhas = 0

    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma única conexão para governar todas
    cursor = connection.cursor() # o cursor rei

    
    while dia < diaFinal:
        diaString = converteTempoString(dia)
        URL = "exemplo.com" + diaString + ".html"
        request = requests.get(url = URL)
        conteudo = 0 # inicializar fora para evitar problemas de falta de inicialização
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, "lxml")
            VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
            try:
                conteudo = VarJson[1].text # Pega o que tem dentro da tag.
                conteudo = conteudo.replace("var json_data=", "") # Tira o "var json_data=" e deixa só as chaves.
                if (conteudo != 0):
                    counteudoAuxiliar = json.loads(conteudo) # vai levar o json para virar objeto
                    counteudoAuxiliar = transformaObjeto(counteudoAuxiliar) # transforma dicionario em objeto
                    inserir = inserirOuNao(counteudoAuxiliar, cursor) # pega esse objeto e vê se o datetime dele existe no SQL.
                if (inserir == 0):
                    insereSQL(conteudo, URL, counteudoAuxiliar, cursor)
                    print ("Conteudo de datetime ", str(counteudoAuxiliar.general.date_time).replace(" -0300", ""), " foi inserido")
                else:
                    modificaSQL(conteudo, inserir, cursor)
                    print ("Conteudo de ID ", inserir, " foi modificado")
        
            #except ValueError as e:
            except:
                #print(e)
                conteudo = None
                numeroFalhas += 1
                print("Erro na formatação do htmtl, os valores do dia " + diaString + " não serão inseridos.")
                print("Ou é erro no SQL.")
        else:
            print("O status/resposta do request que no dia " + diaString + " deu erro, é: " + str(request.status_code))  # dá 404 quando não achar, só fazer assim para verificar as datas inexistentes.
        
        dia = dia + tempoSoma # para parar o while, soma os dias (objetos dia)
    
    connection.commit()
    
    print("Ocorreram " + str(numeroFalhas) + " falhas")
    print("Agora que foi feito a atualização dos jsons, iniciamos a atualização das outras tables.")
    altera_tables(cursor)
    cursor.fetchall() # evitar unread value
    connection.commit()
    cursor.close()
    connection.close()
    print("Codigo finalizado")

def selectSQL(cursor): # Pega todos os jsons da table e coloca numa lista

    codigoSQL = "SELECT Json FROM json where id > 0;" # pega todos os valores json
    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    resultadosJson = []
    for json in resultado:
        resultadosJson.append(json[0]) # Coloco o valor json da lista resultado na lista resultadosJson
    print("Pegamos os jsons e agora retornamos eles")
    return resultadosJson


def altera_tables(cursor):
    lista_jsons = selectSQL(cursor)
    ID_atual = 1 # O ID vai representar o ID de cada Json extraido.
    for valor_json in lista_jsons:
        dicionario_json = json.loads(valor_json)
        objeto_json = transformaObjeto(dicionario_json)
        altera_general(cursor, ID_atual, objeto_json) # codigo já funcional
        altera_requests(cursor, ID_atual, objeto_json)
        ID_atual = ID_atual + 1


def altera_requests(cursor, ID_ATUAl, objeto):
    cursor.fetchall() # evitar unread value
    codigoSQL = "SELECT id from dashboard_requests WHERE json_id = %s"
    cursor.execute(codigoSQL, (ID_ATUAl,))
    resultado = cursor.fetchone() # o fetchall sempre vai retornar algo, mesmo se for uma lista vazia, não é none igual o fetchone.
    print("O resultado do altera_requests: ", resultado)

    if resultado is None: # Se ele achou um ID igual, ignora. Se ele achou algo que não é um ID igual, insere o novo ID que não existe ainda
        # Importante considerar que o fetchone pode retornar none. Mas não tira todos os valores da fila, 
        # por isso no inicio colocamos um cursor.fetchall para evitar conflito.
        for data in objeto.requests.data:
            data = transformaObjeto(data)
            codigoSQL = """
            INSERT INTO dashboard_requests(json_id, hits_count, hits_percent, visitors_count, visitors_percent,
            bytes_count, bytes_percent, data, method, protocol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (str(ID_ATUAl), str(data.hits.count), str(data.hits.percent), str(data.visitors.count),
                       str(data.visitors.percent), str(data.bytes.count), str(data.bytes.percent),
                       str(data.data), str(data.method), str(data.protocol))

            cursor.execute(codigoSQL, valores)

        print("Os valores de ID: ", ID_ATUAl, " não existiam e foram inseridos (dashboard requests)")
    else:
        print("Os valores de ID: ", ID_ATUAl, " já existem (dashboard requests)")




def altera_general(cursor, ID, objeto):
    cursor.fetchall() # evitar unread value
    codigoSQL = "SELECT id from dashboard_general WHERE id = %s"
    cursor.execute(codigoSQL, (ID,)) # para mais de um valor, usamos uma tupla para preencher os %s
    resultado = cursor.fetchone()
    print("O fetchone de valor ", resultado, "é o resultado, o ID de valor ", ID, "foi procurado")
    #"""
    if resultado is None: # Se não existe nenhum id que seja igual a um id dos novos jsons, insere esse id
        codigoSQL = """
        INSERT INTO dashboard_general (json_id, start_date, end_date, date_time, total_requests, 
        valid_requests, failed_requests, generation_time, unique_visitors, unique_files, excluded_hits, 
        unique_referrers, not_found, unique_static_files, log_size, bandwidth, log_path) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
        """
        valores = (str(ID), str(objeto.general.start_date), str(objeto.general.end_date), str(objeto.general.date_time),
            str(objeto.general.total_requests), str(objeto.general.valid_requests), str(objeto.general.failed_requests),
            str(objeto.general.generation_time), str(objeto.general.unique_visitors), str(objeto.general.unique_files),
            str(objeto.general.excluded_hits), str(objeto.general.unique_referrers), str(objeto.general.unique_not_found),
            str(objeto.general.unique_static_files), str(objeto.general.log_size), str(objeto.general.bandwidth),
            str(objeto.general.log_path))
        
        print("Vamos inserir o valor de ID ", ID, "na table")
        cursor.execute(codigoSQL, valores)

        
        print("O valor de ID: ", ID, " não existe e foi inserido (dashboard general)")
        return
    else:
        print("O valor de ID: ", ID, " já existe (dashboard general)")
        return
    #"""   
    

iniciar()
