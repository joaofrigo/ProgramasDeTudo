import requests
from bs4 import BeautifulSoup
import datetime
import mysql.connector

def insereSQL(conteudo, URL):
    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma função que usa um dicionário como argumento

    cursor = connection.cursor()
    codigoSQL = "INSERT INTO json (json, url) VALUES (%s, %s);"
    informacao = (conteudo, URL) # o valor do json e a URL

    cursor.execute(codigoSQL, informacao)
    connection.commit()

    cursor.close()
    connection.close()

def inserirOuNao(counteudo):
    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma função que usa um dicionário como argumento

    cursor = connection.cursor()
    codigoSQL = "SELECT FROM json "

def converteTempoString(dia):
    dia = str(dia) # transforma em string
    dia = dia.split("-") # tira os traços
    dia = ''.join(dia) # concatena os valores. soma '' mais um valor da lista e reitera.
    return dia

dia = datetime.date(2020, 1, 9) # o inicio dos tempos.
diaFinal = datetime.date.today() # o dia hipotético final.
tempoSoma = datetime.timedelta(days= 1)
numeroFalhas = 0
while dia < diaFinal:
    diaString = converteTempoString(dia)
    URL = "exemplo.com/" + diaString + ".html"
    request = requests.get(url = URL)
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "lxml")
        VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
        try:
            conteudo = VarJson[1].text # Pega o que tem dentro da tag.
            conteudo = conteudo.replace("var json_data=", "") # Tira o "var json_data=" e deixa só as chaves.
            # Colocar o if se existe antes do insereSQL, se não existe dá insere, se existe modifica.
            #insereOuNao(conteudo)
            insereSQL(conteudo, URL)
        except:
            conteudo = None
            numeroFalhas += 1
            print("Erro na formatação do htmtl, os valores do dia " + diaString + " não serão inseridos.")
            print("Ou é erro no SQL.")
    else:
        print("O status/resposta do request que no dia " + diaString + " deu erro, é: " + str(request.status_code))  # dá 404 quando não achar, só fazer assim para verificar as datas inexistentes.
    dia = dia + tempoSoma # para parar o while, soma os dias (objetos dia)
print("Ocorreram " + str(numeroFalhas) + " falhas")