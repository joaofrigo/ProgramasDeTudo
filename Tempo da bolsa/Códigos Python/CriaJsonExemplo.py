import requests
from bs4 import BeautifulSoup
import datetime

def converteTempoString(dia):
    dia = str(dia) # transforma em string
    dia = dia.split("-") # tira os traços
    dia = ''.join(dia) # concatena os valores. soma '' mais um valor da lista e reitera.
    return dia

diaFinal = datetime.date.today()
tempoSoma = datetime.timedelta(days= 1)
dia = datetime.date.today() - tempoSoma
numeroFalhas = 0
while dia < diaFinal:
    diaString = converteTempoString(dia)
    URL = "exemplo.com/" + diaString + ".html"
    request = requests.get(url = URL)
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "lxml")
        VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
        nomeArquivo = "Arquivo Json do dia " + diaString
        try:
            conteudo = VarJson[1].text # Pega o que tem dentro da tag.
            conteudo = conteudo.replace("var json_data=", "") # Tira o "var json_data=" e deixa só as chaves.
        except:
            conteudo = None
            numeroFalhas += 1
            nomeArquivo = "Arquivo falho no dia " + diaString + " Problema na formatação do html"
        with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(str(conteudo))
    else:
        print("O status/resposta do request que no dia " + diaString + " deu erro, é: " + str(request.status_code))  # dá 404 quando não achar, só fazer assim para verificar as datas inexistentes.
    dia = dia + tempoSoma # para parar o while, soma os dias (objetos dia)
print("Ocorreram " + str(numeroFalhas) + " falhas")