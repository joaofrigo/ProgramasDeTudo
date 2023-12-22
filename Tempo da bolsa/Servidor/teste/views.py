from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from datetime import datetime, date
from django.core.paginator import Paginator

batata = input()
# Nesse arquivo nós fazemos a interação do back end para com o front end do DJANGO. Selects e inserir em objetos para mandar para o DJANGO.

def hello_world(request):
    return HttpResponse("Hello World")

def hello_template(request):
    return render(request, "hello_template")

def teste_html(request):
    return render(request, "teste.html")

def home_django(request):
    return render(request, "homeDjango.html", {"nome": "batatoncio"}) # o plot é que se pode passar um dicionário para um html usar


class Dashboard:
    def __init__(self, total_requests=0, valid_requests=0, unique_files =0, failed_requests=0,
                 not_found=0, unique_visitors=0, unique_referrers=0, generation_time=0, unique_static_files=0,
                 excluded_hits=0, log_size=0, bandwidth=0):
        # valores da dashboard general:
        self.total_requests = total_requests
        self.valid_requests = valid_requests
        self.unique_files  = unique_files 
        self.failed_requests = failed_requests
        self.not_found = not_found
        self.unique_visitors = unique_visitors
        self.unique_referrers = unique_referrers
        self.generation_time = generation_time
        self.unique_static_files = unique_static_files
        self.excluded_hits = excluded_hits
        self.log_size = log_size
        self.bandwidth = bandwidth

        self.requests = []
        self.http_status_codes = []

class dashboard_requests:  # Você deve usar "class" para definir uma classe
    def __init__(self, hits_count=0, hits_percent=0, visitors_count=0, visitors_percent=0, bytes_count=0,
                 bytes_percent=0, data=0, method=0, protocol=0):
        self.hits_count = hits_count
        self.hits_percent = hits_percent
        self.visitors_count = visitors_count
        self.visitors_percent = visitors_percent
        self.bytes_count = bytes_count
        self.bytes_percent = bytes_percent
        self.data = data
        self.method = method
        self.protocol = protocol

class dashboard_http_status_codes:  # Você deve usar "class" para definir uma classe
    def __init__(self, hits_count=0, hits_percent=0, visitors_count=0, visitors_percent=0, bytes_count=0,
                 bytes_percent=0, data=0, items = None):
        self.hits_count = hits_count
        self.hits_percent = hits_percent
        self.visitors_count = visitors_count
        self.visitors_percent = visitors_percent
        self.bytes_count = bytes_count
        self.bytes_percent = bytes_percent
        self.data = data
        self.items = []




def dashboard_general(request):
    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma função que usaa um dicionário como argumento

    cursor = connection.cursor()
    dicionario = {"data": Dashboard(), "page_objeto": None, "page_objeto_2": None} # Depois é só colocar um [] aqui, para criar uma lista de objetos com um for
    # que vai determinar o tamanho de quantas vezes vai ser reiterado pela quantidade de IDS diferentes
    # o indexador serve para retirar da tupla

    # diaMarco0 = 20200420; // o dia de inicio do dashboard,
    
    # preciso colocar uma inicialização de data no tempalte. Sempre vai ter uma data no template assim.
    # Vou verificar se existe um request, se ele existe troca a data, se não, inicializa de maneira padrão.
    # jà que não existe data no dashboard_general, mas existe data no json e os dois tem mesmo ID, só fazer
    # Um join para pegar a data do dashboard general e fazer o if de tanto até quanto. Sempre fazemos esse
    # If, só que com as datas iniciais caso não tenha request.
    offset = 0 # valor da paginação.
    hoje = date.today()
    inicio = datetime(2020, 4, 20)
    fim = datetime(hoje.year, hoje.month, hoje.day)
    if request.method == "POST": # Valores dos posts, tanto em paginção, como forms.
        if request.POST.get('inicio'):
            inicio = request.POST.get("inicio")
        if request.POST.get('fim'):
            fim = request.POST.get("fim")
        #if request.POST.get("offset"):
        #    offset = request.POST.get("offset")

    dashboard_general_func(dicionario, cursor, inicio, fim) # Só precisa modificar os valores do dicionário, no caso, adicionar valores
    dashboard_requests_func(dicionario, cursor) # Só precisa modificar os valores do dicionário, no caso, adicionar valores
    dashboard_http_status_codes_func(dicionario, cursor) # Só precisa modificar os valores do dicionário, no caso, adicionar valores
 
    # Agora mexemos com as paginações: page_objeto, page_objeto_2 (...)
    paginator = Paginator(dicionario["data"].requests, 15) # Colocamos o valor dentro de uma "página", considerando a pagina atual do Paginator
    paginator_2 = Paginator(dicionario["data"].http_status_codes, 15)
    pagina_numero = request.GET.get("page") # Pegamos a página atual
    pagina_numero_2 = request.GET.get("page_2")
    page_objeto = paginator.get_page(pagina_numero) # Colocamos a página real no objeto.
    page_objeto_2 = paginator_2.get_page(pagina_numero_2)
    dicionario["page_objeto"] = page_objeto
    dicionario["page_objeto_2"] = page_objeto_2

    # Fechamos a conexão ?
    cursor.close()
    connection.close()
    return render(request, "dashboard_general.html", dicionario)

def dashboard_http_status_codes_func(dicionario, cursor):
    # Estou agrupando todos os valores de um mesmo data, expondo todos os tipos de http_status_codes juntos com o sum
    codigoSQL = f"""
    SELECT sum(hits_count), sum(hits_percent), sum(visitors_count), sum(visitors_percent), 
    sum(bytes_count) , sum(bytes_percent), data, id
    FROM ntelogs.dashboard_status_codes GROUP BY data;
    """
    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    # ordem de valores da tupla: hitcoount, hitpercent, visitorcount, visitorpercent, bytecount, bytepercent, data
    for tupla in resultado:
        codigoSQL = f"""
        SELECT * FROM ntelogs.items_status_codes
        WHERE {tupla[7]} = items_status_codes.id_status_codes
        """
        cursor.execute(codigoSQL) # Código retorna todos os items relacionados ao ID específico de um http_status_codes
        resultado_status = cursor.fetchall() # É uma tupla
        objeto = dashboard_http_status_codes(int(tupla[0]), round(tupla[1], 2), int(tupla[2]), round(tupla[3], 2), int(tupla[4]), round(tupla[5], 2), 
                                             tupla[6], resultado_status) # inicializa o objeto com os valores das tupla.
        dicionario["data"].http_status_codes.append(objeto)

'''
lógica possível para o http_status_codes
def dashboard_http_status_codes_func(dicionario, cursor):
    # Estou agrupando todos os valores de um mesmo data, expondo todos os tipos de http_status_codes juntos com o sum dos items.
    # existem 14 valores em cada tupla, 7 do http_status_codes e 7 considerando o items_status_codes
    codigoSQL = f"""
    SELECT
        dsc.data,
        SUM(dsc.hits_count) AS total_dashboard_hits,
        SUM(dsc.hits_percent) AS total_hits_percent,
        SUM(dsc.bytes_count) AS total_dashboard_bytes,
        SUM(dsc.bytes_percent) AS total_dashboard_bytes_percent,
        SUM(dsc.visitors_count) AS total_dashboard_visitors,
        SUM(dsc.visitors_percent) AS total_dashboard_visitors_percent,
		isc.data AS items_data,
        SUM(isc.hits_count) AS total_items_hits,
        SUM(isc.hits_percent) AS total_items_hits_percent,
        SUM(isc.bytes_count) AS total_items_bytes,
        SUM(isc.bytes_percent) AS total_items_bytes_percent,
        SUM(isc.visitors_count) AS total_items_visitors_hits,
        SUM(isc.visitors_percent) AS total_items_visitors_percent
    FROM
        dashboard_status_codes dsc
    JOIN
        items_status_codes isc ON dsc.id = isc.id_status_codes
    GROUP BY
        dsc.data;
    """
    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    # ordem de valores da tupla: hitcoount, hitpercent, visitorcount, visitorpercent, bytecount, bytepercent, data
    for tupla in resultado:
        #codigoSQL = f"""
        #SELECT * FROM ntelogs.items_status_codes
        #WHERE {tupla[7]} = items_status_codes.id_status_codes
        #"""
        #cursor.execute(codigoSQL) # Código retorna todos os items relacionados ao ID específico de um http_status_codes
        #resultado_status = cursor.fetchall() # É uma tupla
        tupla_items = (tupla[7], int(tupla[8]), round(tupla[9], 2), int(tupla[10]), round(tupla[11], 2), int(tupla[12]), round(tupla[13], 2))
        objeto = dashboard_http_status_codes(tupla[0], int(tupla[1]), round(tupla[2], 2), int(tupla[3]), round(tupla[4], 2), int(tupla[5]), 
                                             round(tupla[6], 2), tupla_items) # inicializa o objeto com os valores das tupla.
        dicionario["data"].http_status_codes.append(objeto)

'''



def dashboard_general_func(dicionario, cursor, inicio, fim):
    codigoSQL = f"""
    SELECT SUM(d.total_requests)
    FROM (
        SELECT dg.total_requests
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].total_requests = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.valid_requests)
    FROM (
        SELECT dg.valid_requests
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].valid_requests = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.unique_files)
    FROM (
        SELECT dg.unique_files 
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].unique_files  = cursor.fetchone()[0]

    codigoSQL = f"""
    SELECT SUM(d.failed_requests)
    FROM (
        SELECT dg.failed_requests
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].failed_requests = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.not_found)
    FROM (
        SELECT dg.not_found
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].not_found = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.unique_visitors)
    FROM (
        SELECT dg.unique_visitors
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].unique_visitors = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.unique_referrers)
    FROM (
        SELECT dg.unique_referrers
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].unique_referrers = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.generation_time)
    FROM (
        SELECT dg.generation_time
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].generation_time = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.unique_static_files)
    FROM (
        SELECT dg.unique_static_files
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].unique_static_files = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.excluded_hits)
    FROM (
        SELECT dg.excluded_hits
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].excluded_hits = int(cursor.fetchone()[0])

    codigoSQL = f"""
    SELECT SUM(d.log_size)
    FROM (
        SELECT dg.log_size
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].log_size = format((cursor.fetchone()[0] / (10**9)), ".2f")

    codigoSQL = f"""
    SELECT SUM(d.bandwidth)
    FROM (
        SELECT dg.bandwidth
        FROM dashboard_general AS dg
        INNER JOIN json AS j ON dg.json_id = j.id
        WHERE j.data BETWEEN '{inicio}' AND '{fim}'
        ORDER BY dg.id
    ) AS d;
    """
    cursor.execute(codigoSQL)
    dicionario["data"].bandwidth = format((cursor.fetchone()[0] / (10**9)), ".2f")

def dashboard_requests_func(dicionario, cursor):
    codigoSQL = f"""
    SELECT sum(hits_count), sum(hits_percent), sum(visitors_count), sum(visitors_percent), 
    sum(bytes_count) , sum(bytes_percent), data, method, protocol
    FROM ntelogs.dashboard_requests GROUP BY data, method, protocol;
    """
    cursor.execute(codigoSQL)
    resultado = cursor.fetchall()
    indexador = 0
    # ordem de valores da tupla: hitcoount, hitpercent, visitorcount, visitorpercent, bytecount, bytepercent, data
    for tupla in resultado:
        objeto = dashboard_requests(int(tupla[0]), round(tupla[1], 2), int(tupla[2]), round(tupla[3], 2), int(tupla[4]), round(tupla[5], 2), tupla[6],
                                    tupla[7], tupla[8]) # inicializa o objeto com os valores da tupla.
        dicionario["data"].requests.append(objeto)
        # só usar tuplas como vetores, nada demais. só colocar fors.
        #self.hits_count = 0
        #self.hits_percent = 0
        #self.visitors_count = 0
        #self.visitors_percent = 0
        #self.bytes_count = 0
        #self.bytes_percent = 0
        #self.data = ""
        #self.method = ""
        #self.protocol = ""

    

def tira_colchetes(palavra):
    print ("tirando colchetes like a boss")

#def outro_link(request):
    #return render(request, "exemplo_link")
"""
requested_files
bandwidth
log_size
excluded_hits
generation_time
unique_static_files
unique_referrers
unique_visitors
not_found
failed_requests
total_requests
"""

'''
def dashboard_general_teste(request):
    connection = mysql.connector.connect(
    host="nte.ufsm.br",
    user="ntelogs",
    password="ntelogs",
    database="ntelogs"
    ) # uma função que usaa um dicionário como argumento

    cursor = connection.cursor()

    #total_requests, valid_requests, failed_requests, not_found, unique_visitors,
#unique_referrers, generation_time, unique_static_files, excluded_hits, log_size, bandwidth, requested_files)

    #codigoSQL = "SELECT id from dashboard_general"
    #cursor.execute(codigoSQL)
    #id_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(total_requests) from dashboard_general"
    cursor.execute(codigoSQL)
    total_requests_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(requested_files) from dashboard_general"
    cursor.execute(codigoSQL)
    requested_files_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(failed_requests) from dashboard_general"
    cursor.execute(codigoSQL)
    failed_requests_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(not_found) from dashboard_general"
    cursor.execute(codigoSQL)
    not_found_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_visitors) from dashboard_general"
    cursor.execute(codigoSQL)
    unique_visitors_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_referrers) from dashboard_general"
    cursor.execute(codigoSQL)
    unique_referrers_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(generation_time) from dashboard_general"
    cursor.execute(codigoSQL)
    generation_time_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_static_files) from dashboard_general"
    cursor.execute(codigoSQL)
    unique_static_files_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(excluded_hits) from dashboard_general"
    cursor.execute(codigoSQL)
    excluded_hits_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(log_size) from dashboard_general"
    cursor.execute(codigoSQL)
    log_size_fetch = cursor.fetchall()

    codigoSQL = "SELECT sum(bandwidth) from dashboard_general"
    cursor.execute(codigoSQL)
    bandwidth_fetch = cursor.fetchall()


    String_gorda = ""
    # Só colocar todas as variáveis nessa string grandona
    for (total_requests, requested_files, failed_requests, not_found, 
     unique_visitors, unique_referrers, generation_time, unique_static_files, 
     excluded_hits, log_size, 
     bandwidth) in zip(total_requests_fetch, 
                    requested_files_fetch, failed_requests_fetch,
                    not_found_fetch, unique_visitors_fetch, 
                    unique_referrers_fetch, generation_time_fetch,
                    unique_static_files_fetch, excluded_hits_fetch, 
                    log_size_fetch, bandwidth_fetch):
    # O código dentro do loop deve estar devidamente indentado
        String_gorda += (f"total_requests: {total_requests}, <br> requested_files: {requested_files}, <br>"
                    f"failed_requests: {failed_requests}, <br> not_found: {not_found}, <br> unique_visitors: {unique_visitors}, <br>"
                    f"unique_referrers: {unique_referrers}, <br> generation_time: {generation_time}, <br>"
                    f"unique_static_files: {unique_static_files}, <br> excluded_hits: {excluded_hits}, <br> log_size: {log_size}, <br>"
                    f"bandwidth: {bandwidth}<br>")


    cursor.close()
    connection.close()

    return HttpResponse(String_gorda)

    '''

    




"""

# Create your views here.
# request -> response
# request handler
#Código que pega tudo bem gordo
"""
"""""
for (id_, total_requests, requested_files, failed_requests, not_found, 
     unique_visitors, unique_referrers, generation_time, unique_static_files, 
     excluded_hits, log_size, 
     bandwidth) in zip(id_fetch, total_requests_fetch, 
                        requested_files_fetch, failed_requests_fetch,
                        not_found_fetch, unique_visitors_fetch, 
                        unique_referrers_fetch, generation_time_fetch,
                        unique_static_files_fetch, excluded_hits_fetch, 
                        log_size_fetch, bandwidth_fetch):
    # O código dentro do loop deve estar devidamente indentado
        String_gorda += (f"ID: {id_}, total_requests: {total_requests}, requested_files: {requested_files}, "
                    f"failed_requests: {failed_requests}, not_found: {not_found}, unique_visitors: {unique_visitors}, "
                    f"unique_referrers: {unique_referrers}, generation_time: {generation_time}, "
                    f"unique_static_files: {unique_static_files}, excluded_hits: {excluded_hits}, log_size: {log_size}, "
                    f"bandwidth: {bandwidth}<br><br>")






dicionario = {"total_requests":0, "requested_files":0, "failed_requests":0, "not_found":0, "unique_visitors":0,
                  "unique_referrers":0, "generation_time":0, "unique_static_files":0, "excluded_hits":0,
                  "log_size":0, "bandwidth":0, "requested_files":0}

    codigoSQL = "SELECT sum(total_requests) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["total_requests"] = cursor.fetchall()

    codigoSQL = "SELECT sum(requested_files) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["requested_files"] = str(cursor.fetchall())
    dicionario["requested_files"] = str(dicionario["requested_files"]).replace(",","")

    codigoSQL = "SELECT sum(failed_requests) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["failed_requests"] = cursor.fetchall()

    codigoSQL = "SELECT sum(not_found) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["not_found"] = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_visitors) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["unique_visitors"] = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_referrers) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["unique_referrers"] = cursor.fetchall()

    codigoSQL = "SELECT sum(generation_time) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["generation_time"] = cursor.fetchall()

    codigoSQL = "SELECT sum(unique_static_files) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["unique_static_files"] = cursor.fetchall()

    codigoSQL = "SELECT sum(excluded_hits) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["excluded_hits"] = cursor.fetchall()

    codigoSQL = "SELECT sum(log_size) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["log_size"] = cursor.fetchall()

    codigoSQL = "SELECT sum(bandwidth) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["bandwidth"] = cursor.fetchall()

    codigoSQL = "SELECT sum(requested_files) from dashboard_general"
    cursor.execute(codigoSQL)
    dicionario["requested_files"] = cursor.fetchall()

    return render(request, "dashboard_general.html", dicionario)
"""""