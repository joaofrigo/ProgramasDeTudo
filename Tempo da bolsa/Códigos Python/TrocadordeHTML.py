from bs4 import BeautifulSoup
import mysql.connector
import json
from collections import namedtuple
import requests
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
HitsVisitor = 0
VisitorsVisitor = 0
TxAmountVisitor = 0
DataVisitor = 0
HitsURL = 0
VisitorsURL = 0
TxAmountURL = 0
DataURL = 0

VisitorVisitor = 0
VisitorHits = 0
VisitorTxAmount = 0
VisitorData = 0
VisitorsHitsMax = 0
VisitorsVisitorsMax = 0
VisitorsTxAmountMax = 0
VisitorsHitsMin = 1000
VisitorsTxAmountMin = 1000
VisitorsVisitorsMin = 1000

URLHits = 0
URLVisitors = 0
URLTxAmount = 0
URLData = 0
URLHitsMax = 0
URLVisitorsMax = 0
URLTxAmountMax = 0
URLHitsMin = 1000
URLVisitorsMin = 1000
URLTxAmountMin = 1000

StaticHits = 0
StaticVisitors = 0
StaticTxamount = 0
StaticData = 0
StaticHitsMax = 0
StaticHitsMin = 1000
StaticVisitorsMax = 0
StaticVisitorsMin = 1000
StaticTxAmountMax = 0
StaticTxAmountMin = 1000

NotFoundHits = 0
NotFoundVisitors = 0
NotFoundTxAmount = 0
NotFoundData = 0
NotFoundHitsMax = 0
NotFoundHitsMin = 1000
NotFoundVisitorsMax = 0
NotfoundVisitorsMin = 1000
NotFoundTxAmountMax = 0
NotfoundTxAmountMin = 1000

VisitorHostHits = 0
VisitorHostTxAmount = 0
VisitorHostVisitors = 0
VisitorHostData = 0
VisitorHostIpHitsMax = 0
VisitorHostIpHitsMin = 1000
VisitorHostVisitorsMax = 0
VisitorsHostVisitorsMin = 1000
VisitorsHostTxAmountMax = 0
VisitorsHostTxAmountMin = 1000

OperatingSysHits = 0
OperatingSysVisitors = 0
OperatingSysData = 0
OperatingSysTxAmount = 0
OperatingSysHitsMax = 0
OperatingSysHitsMin = 1000
OperatingSysVisitorsMax = 0
OperatingSysVisitorsMin = 1000
OperatingSysTxAmountMax = 0
OperatingSysTxAMountMin = 1000

BrowsersHits = 0
BrowsersVisitors = 0
BrowsersTxAmount = 0
BrowsersData = 0
BrowsersHitsMax = 0
BrowsersHitsMin = 1000
BrowsersVisitorsMax = 0
BrowsersVisitorsMin = 1000
BrowsersTxAmountMax = 0
BrowsersTxAmountMin = 1000

TimeDistrHits = 0
TimeDistrTxAmount = 0
TimeDistrVisitors = 0
TimeDistrData = 0
TimeDistrHitsMax = 0
TimeDistrHitsMin = 1000
TimeDistrVisitorsMax = 0
TimeDistrVisitorsMin = 1000
TimeDistrTxAmountMax = 0
TimeDistrTxAmountMin = 1000

RefferSitesHits = 0
RefferSitesVisitors = 0
RefferSitesTxAmount = 0
RefferSitesData = 0
RefferSitesHitsMax = 0
RefferSitesHitsMin = 1000
RefferSitesVisitorsMax = 0
RefferSitesVisitorsMin = 1000
RefferSitesTxAmountMax = 0
RefferSitesTxAmountMin = 1000

HttpStatCodesHits = 0
HttpStatCodesVisitors = 0
HttpStatCodesData = 0
HttpStatCodesTxAmount = 0
HttpStatCodesHitsMax = 0
HttpStatCodesHitsMin = 1000
HttpStatCodesVisitorsMax = 0
HttpStatCodesVisitorsMin = 1000
HttpStatCodesTxAmountMax = 0
HttpStatCodesTxAmountMin = 1000

GeoLocHits = 0
GeoLocVisitors = 0
GeoLocTxAmount = 0
GeolocData = 0
GeoLocHitsMax = 0
GeoLocHitsMin = 1000
GeoLocVisitorsMax = 0
GeoLocVisitorsMin = 1000
GeoLocTxAmountMax = 0
GeoLocTxAmountMin = 1000

#Preciso criar os vetores dos data.
DataGeo = []
DataBrowsers = []
DataHosts = []
DataNotFound = []
DataOs = []
DataReferring = []
DataRequests = []
DataStaticRequests = []
DataStatusCodes = []
DataVisitTime = []
DataVisitors = []


# variaveis que serão somadas.

def selectSQL():
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
          "\nTxAmount:", TxAmount,
          "\nHitsVisitor:", HitsVisitor,
          "\nVisitorsVisitor:", VisitorsVisitor,
          "\nTxAmountVisitor:", TxAmountVisitor,
          "\nDataVisitor:", DataVisitor,
          "\nHitsURL:", HitsURL,
          "\nVisitorsURL:", VisitorsURL,
          "\nTxAmountURL:", TxAmountURL,
          "\nDataURL", DataURL,
          "\nGrandeDataURLVisitorsMax", URLVisitorsMax)

def somaValores(objeto):
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

    global HitsVisitor
    global VisitorsVisitor
    global TxAmountVisitor
    global DataVisitor
    global HitsURL
    global VisitorsURL
    global TxAmountURL
    global DataURL

    global VisitorsVisitorsMax
    global VisitorsHitsMax
    global VisitorsTxAmountMax

    global URLTxAmountMax
    global URLHitsMax
    global URLVisitorsMax

    global VisitorsHitsMin
    global VisitorsTxAmountMin
    global VisitorsVisitorsMin

    global URLHitsMin
    global URLVisitorsMin
    global URLTxAmountMin

    global StaticHits
    global StaticVisitors
    global StaticTxamount
    global StaticData
    global StaticHitsMax
    global StaticHitsMin
    global StaticVisitorsMax
    global StaticVisitorsMin
    global StaticTxAmountMax
    global StaticTxAmountMin

    global NotFoundHits
    global NotFoundTxAmount
    global NotFoundData
    global NotFoundVisitors
    global NotfoundTxAmountMin
    global NotFoundTxAmountMax
    global NotFoundVisitorsMax
    global NotfoundVisitorsMin
    global NotFoundHitsMax
    global NotFoundHitsMin

    global VisitorHostHits
    global VisitorHostVisitors
    global VisitorHostData
    global VisitorHostTxAmount
    global VisitorHostIpHitsMax
    global VisitorHostIpHitsMin
    global VisitorsHostVisitorsMin
    global VisitorHostVisitorsMax
    global VisitorsHostTxAmountMax
    global VisitorsHostTxAmountMin

    global OperatingSysData
    global OperatingSysVisitors
    global OperatingSysHits
    global OperatingSysTxAmount
    global OperatingSysHitsMax
    global OperatingSysHitsMin
    global OperatingSysTxAmountMax
    global OperatingSysTxAMountMin
    global OperatingSysVisitorsMin
    global OperatingSysVisitorsMax

    global BrowsersData
    global BrowsersVisitors
    global BrowsersTxAmount
    global BrowsersHits
    global BrowsersHitsMax
    global BrowsersHitsMin
    global BrowsersVisitorsMax
    global BrowsersVisitorsMin
    global BrowsersTxAmountMax
    global BrowsersTxAmountMin

    global TimeDistrData
    global TimeDistrHits
    global TimeDistrTxAmount
    global TimeDistrVisitors
    global TimeDistrHitsMax
    global TimeDistrHitsMin
    global TimeDistrTxAmountMax
    global TimeDistrTxAmountMin
    global TimeDistrVisitorsMax
    global TimeDistrVisitorsMin

    global RefferSitesData
    global RefferSitesHits
    global RefferSitesVisitors
    global RefferSitesTxAmount
    global RefferSitesHitsMax
    global RefferSitesHitsMin
    global RefferSitesTxAmountMax
    global RefferSitesTxAmountMin
    global RefferSitesVisitorsMax
    global RefferSitesVisitorsMin

    global HttpStatCodesData
    global HttpStatCodesHits
    global HttpStatCodesTxAmount
    global HttpStatCodesVisitors
    global HttpStatCodesHitsMax
    global HttpStatCodesHitsMin
    global HttpStatCodesTxAmountMax
    global HttpStatCodesTxAmountMin
    global HttpStatCodesVisitorsMax
    global HttpStatCodesVisitorsMin

    global GeolocData
    global GeoLocHits
    global GeoLocVisitors
    global GeoLocTxAmount
    global GeoLocHitsMax
    global GeoLocHitsMin
    global GeoLocVisitorsMax
    global GeoLocVisitorsMin
    global GeoLocTxAmountMax
    global GeoLocTxAmountMin

    global DataBrowsers
    global DataGeo
    global DataHosts
    global DataNotFound
    global DataOs
    global DataReferring
    global DataRequests
    global DataStatusCodes
    global DataVisitors
    global DataStaticRequests
    global DataURL    
    global DataVisitTime

    TotalRequests = TotalRequests + objeto.general.total_requests
    ValidRequests = ValidRequests + objeto.general.valid_requests
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

    #print(objeto.visitors.metadata.hits)
    # Somo as variaveis máximas

    HitsVisitor = HitsVisitor + objeto.visitors.metadata.hits.count
    VisitorsVisitor = VisitorsVisitor + objeto.visitors.metadata.visitors.count
    TxAmountVisitor = TxAmountVisitor + objeto.visitors.metadata.bytes.count
    DataVisitor = DataVisitor + objeto.visitors.metadata.data.unique

    HitsURL = HitsURL + objeto.requests.metadata.hits.count
    VisitorsURL = VisitorsURL + objeto.requests.metadata.visitors.count
    TxAmountURL = TxAmountURL + objeto.requests.metadata.bytes.count
    DataURL = DataURL + objeto.requests.metadata.data.unique

    BrowsersData = BrowsersData + objeto.browsers.metadata.data.unique
    BrowsersHits = BrowsersHits + objeto.browsers.metadata.hits.count
    BrowsersTxAmount = BrowsersTxAmount + objeto.browsers.metadata.bytes.count
    BrowsersVisitors = BrowsersVisitors + objeto.browsers.metadata.visitors.count

    GeolocData = GeolocData + objeto.geolocation.metadata.data.unique
    GeoLocHits = GeoLocHits + objeto.geolocation.metadata.hits.count
    GeoLocTxAmount = GeoLocTxAmount + objeto.geolocation.metadata.bytes.count
    GeoLocVisitors = GeoLocVisitors + objeto.geolocation.metadata.visitors.count

    VisitorHostVisitors = VisitorHostVisitors + objeto.hosts.metadata.visitors.count
    VisitorHostData = VisitorHostData + objeto.hosts.metadata.data.unique
    VisitorHostHits = VisitorHostHits + objeto.hosts.metadata.hits.count
    VisitorHostTxAmount = VisitorHostTxAmount + objeto.hosts.metadata.bytes.count

    NotFoundHits = NotFoundHits + objeto.not_found.metadata.hits.count
    NotFoundVisitors = NotFoundVisitors + objeto.not_found.metadata.visitors.count
    NotFoundData = NotFoundData + objeto.not_found.metadata.data.unique
    NotFoundTxAmount = NotFoundTxAmount + objeto.not_found.metadata.bytes.count

    OperatingSysHits = OperatingSysHits + objeto.os.metadata.hits.count
    OperatingSysData = OperatingSysData + objeto.os.metadata.data.unique
    OperatingSysVisitors = OperatingSysVisitors + objeto.os.metadata.visitors.count
    OperatingSysTxAmount = OperatingSysTxAmount + objeto.os.metadata.bytes.count

    RefferSitesData = RefferSitesData + objeto.referring_sites.metadata.data.unique
    RefferSitesHits = RefferSitesHits + objeto.referring_sites.metadata.hits.count
    RefferSitesVisitors = RefferSitesVisitors + objeto.referring_sites.metadata.visitors.count
    RefferSitesTxAmount = RefferSitesTxAmount + objeto.referring_sites.metadata.bytes.count

    StaticData = StaticData + objeto.static_requests.metadata.data.unique
    StaticVisitors = StaticVisitors + objeto.static_requests.metadata.visitors.count
    StaticTxamount = StaticTxamount + objeto.static_requests.metadata.bytes.count
    StaticHits = StaticHits + objeto.static_requests.metadata.hits.count

    HttpStatCodesData = HttpStatCodesData + objeto.status_codes.metadata.data.unique
    HttpStatCodesHits = HttpStatCodesHits + objeto.status_codes.metadata.hits.count
    HttpStatCodesVisitors = HttpStatCodesVisitors + objeto.status_codes.metadata.visitors.count
    HttpStatCodesTxAmount = HttpStatCodesTxAmount + objeto.status_codes.metadata.bytes.count

    TimeDistrData = TimeDistrData + objeto.visit_time.metadata.data.unique
    TimeDistrHits = TimeDistrHits + objeto.visit_time.metadata.hits.count
    TimeDistrTxAmount = TimeDistrTxAmount + objeto.visit_time.metadata.bytes.count
    TimeDistrVisitors = TimeDistrVisitors + objeto.visit_time.metadata.visitors.count

    # Cria o vetor data gigante:
    DataGeo.extend(objeto.geolocation.data)
    DataBrowsers.extend(objeto.browsers.data)
    DataHosts.extend(objeto.hosts.data)
    DataNotFound.extend(objeto.not_found.data)
    DataOs.extend(objeto.os.data)
    DataReferring.extend(objeto.referring_sites.data)
    DataRequests.extend(objeto.requests.data)
    DataStaticRequests.extend(objeto.static_requests.data)
    DataStatusCodes.extend(objeto.status_codes.data)
    DataVisitTime.extend(objeto.visit_time.data)
    DataVisitors.extend(objeto.visitors.data) 


    ##### preencho os max e os minimos reais, comparando os máximos e mínimos de fato.
    ##############################

    if(URLVisitorsMax < objeto.requests.metadata.visitors.max):
        URLVisitorsMax = objeto.requests.metadata.visitors.max
    if(URLHitsMax < objeto.requests.metadata.hits.max):
        URLHitsMax = objeto.requests.metadata.visitors.max
    if(URLTxAmountMax < objeto.requests.metadata.bytes.max):
        URLTxAmountMax = objeto.requests.metadata.bytes.max

    if(VisitorsHitsMax < objeto.visitors.metadata.hits.max):
        VisitorsHitsMax = objeto.visitors.metadata.hits.max
    if(VisitorsTxAmountMax < objeto.visitors.metadata.bytes.max):
        VisitorsTxAmountMax = objeto.visitors.metadata.bytes.max
    if(VisitorsVisitorsMax < objeto.visitors.metadata.visitors.max):
        VisitorsVisitorsMax = objeto.visitors.metadata.visitors.max

    if(StaticVisitorsMax < objeto.static_requests.metadata.visitors.max):
        StaticVisitorsMax = objeto.static_requests.metadata.visitors.max

    if(StaticVisitorsMin > objeto.static_requests.metadata.visitors.min):
        StaticVisitorsMin = objeto.static_requests.metadata.visitors.min

    if(StaticHitsMax < objeto.static_requests.metadata.hits.max):
        StaticHitsMax = objeto.static_requests.metadata.hits.max

    if(StaticHitsMin > objeto.static_requests.metadata.hits.min):
        StaticHitsMin = objeto.static_requests.metadata.hits.min

    if(StaticTxAmountMax < objeto.static_requests.metadata.bytes.max):
        StaticTxAmountMax = objeto.static_requests.metadata.bytes.max

    if(StaticTxAmountMin > objeto.static_requests.metadata.bytes.min):
        StaticTxAmountMin = objeto.static_requests.metadata.bytes.min

    if(NotfoundTxAmountMin > objeto.not_found.metadata.bytes.min):
        NotfoundTxAmountMin = objeto.static_requests.metadata.bytes.min
    if(NotFoundTxAmountMax < objeto.not_found.metadata.bytes.max):
        NotFoundTxAmountMax = objeto.not_found.metadata.bytes.max
    if(NotfoundVisitorsMin > objeto.not_found.metadata.visitors.min):
        NotfoundVisitorsMin = objeto.not_found.metadata.visitors.min
    if(NotFoundVisitorsMax < objeto.not_found.metadata.visitors.max):
        NotFoundVisitorsMax = objeto.not_found.metadata.visitors.max
    if(NotFoundHitsMax > objeto.not_found.metadata.hits.max):
        NotFoundHitsMax = objeto.not_found.metadata.hits.max
    if(NotFoundHitsMin < objeto.not_found.metadata.hits.min):
        NotFoundHitsMin = objeto.not_found.metadata.hits.min

    if(VisitorHostIpHitsMax < objeto.hosts.metadata.hits.max):
        VisitorHostIpHitsMax = objeto.hosts.metadata.hits.max
    if(VisitorHostIpHitsMin > objeto.hosts.metadata.hits.min):
        VisitorHostIpHitsMin = objeto.hosts.metadata.hits.min
    if(VisitorHostVisitorsMax < objeto.hosts.metadata.visitors.max):
        VisitorHostVisitorsMax = objeto.hosts.metadata.visitors.max
    if(VisitorsHostVisitorsMin > objeto.hosts.metadata.visitors.min):
        VisitorsHostVisitorsMin = objeto.hosts.metadata.visitors.min
    if(VisitorsHostTxAmountMin > objeto.hosts.metadata.bytes.min):
        VisitorsHostTxAmountMin = objeto.hosts.metadata.visitors.min
    if(VisitorsHostTxAmountMax < objeto.hosts.metadata.bytes.max):
        VisitorsHostTxAmountMax = objeto.hosts.metadata.bytes.max

    if(OperatingSysHitsMax < objeto.os.metadata.hits.max):
        OperatingSysHitsMax = objeto.os.metadata.hits.max
    if(OperatingSysHitsMin > objeto.os.metadata.hits.min):
        OperatingSysHitsMin = objeto.os.metadata.hits.min
    if(OperatingSysTxAmountMax < objeto.os.metadata.bytes.max):
        OperatingSysTxAmountMax = objeto.os.metadata.bytes.max
    if(OperatingSysTxAMountMin > objeto.os.metadata.bytes.min):
        OperatingSysTxAMountMin = objeto.os.metadata.bytes.min
    if(OperatingSysVisitorsMax < objeto.os.metadata.visitors.max):
        OperatingSysVisitorsMax = objeto.os.metadata.visitors.max
    if(OperatingSysVisitorsMin > objeto.os.metadata.visitors.min):
        OperatingSysVisitorsMin = objeto.os.metadata.visitors.min

    if(BrowsersHitsMax < objeto.browsers.metadata.hits.max):
        BrowsersHitsMax = objeto.browsers.metadata.hits.max
    if(BrowsersHitsMin > objeto.browsers.metadata.hits.min):
        BrowsersHitsMin = objeto.browsers.metadata.hits.min
    if(BrowsersVisitorsMax < objeto.browsers.metadata.visitors.max):
        BrowsersVisitorsMax = objeto.browsers.metadata.visitors.max
    if(BrowsersVisitorsMin > objeto.browsers.metadata.visitors.min):
        BrowsersVisitorsMin = objeto.browsers.metadata.visitors.min
    if(BrowsersTxAmountMax < objeto.browsers.metadata.bytes.max):
        BrowsersTxAmountMax = objeto.browsers.metadata.bytes.max
    if(BrowsersTxAmountMin > objeto.browsers.metadata.bytes.min):
        BrowsersTxAmountMin = objeto.browsers.metadata.bytes.min

    if(TimeDistrHitsMax < objeto.visit_time.metadata.hits.max):
        TimeDistrHitsMax = objeto.visit_time.metadata.hits.max
    if(TimeDistrHitsMin > objeto.visit_time.metadata.hits.min):
        TimeDistrHitsMin = objeto.visit_time.metadata.hits.min
    if(TimeDistrTxAmountMax < objeto.visit_time.metadata.bytes.max):
        TimeDistrTxAmountMax = objeto.visit_time.metadata.bytes.max
    if(TimeDistrTxAmountMin > objeto.visit_time.metadata.bytes.min):
        TimeDistrTxAmountMin = objeto.visit_time.metadata.bytes.min
    if(TimeDistrVisitorsMax < objeto.visit_time.metadata.visitors.max):
        TimeDistrVisitorsMax = objeto.visit_time.metadata.visitors.max
    if(TimeDistrVisitorsMin > objeto.visit_time.metadata.visitors.min):
        TimeDistrVisitorsMin = objeto.visit_time.metadata.visitors.min

    if(RefferSitesHitsMax < objeto.referring_sites.metadata.hits.max):
        RefferSitesHitsMax = objeto.referring_sites.metadata.hits.max
    if(RefferSitesHitsMin > objeto.referring_sites.metadata.hits.min):
        RefferSitesHitsMin = objeto.referring_sites.metadata.hits.min
    if(RefferSitesVisitorsMax < objeto.referring_sites.metadata.visitors.max):
        RefferSitesVisitorsMax = objeto.referring_sites.metadata.visitors.max
    if(RefferSitesVisitorsMin > objeto.referring_sites.metadata.visitors.min):
        RefferSitesVisitorsMin =  objeto.referring_sites.metadata.visitors.min
    if(RefferSitesTxAmountMax < objeto.referring_sites.metadata.bytes.max):
        RefferSitesTxAmountMax = objeto.referring_sites.metadata.bytes.max
    if(RefferSitesTxAmountMin > objeto.referring_sites.metadata.bytes.min):
        RefferSitesTxAmountMin = objeto.referring_sites.metadata.bytes.min

    if(HttpStatCodesHitsMax < objeto.status_codes.metadata.hits.max):
        HttpStatCodesHitsMax = objeto.status_codes.metadata.hits.max
    if(HttpStatCodesHitsMin > objeto.status_codes.metadata.hits.min):
        HttpStatCodesHitsMin = objeto.status_codes.metadata.hits.min
    if(HttpStatCodesTxAmountMax < objeto.status_codes.metadata.bytes.max):
        HttpStatCodesTxAmountMax = objeto.status_codes.metadata.bytes.max
    if(HttpStatCodesTxAmountMin > objeto.status_codes.metadata.bytes.min):
        HttpStatCodesTxAmountMin = objeto.status_codes.metadata.bytes.min
    if(HttpStatCodesVisitorsMax < objeto.status_codes.metadata.visitors.max):
        HttpStatCodesVisitorsMax = objeto.status_codes.metadata.visitors.max
    if(HttpStatCodesVisitorsMin > objeto.status_codes.metadata.visitors.min):
        HttpStatCodesVisitorsMin = objeto.status_codes.metadata.visitors.min

    if(GeoLocHitsMax < objeto.geolocation.metadata.hits.max):
        GeoLocHitsMax = objeto.geolocation.metadata.hits.max
    if(GeoLocHitsMin > objeto.geolocation.metadata.hits.min):
        GeoLocHitsMin = objeto.geolocation.metadata.hits.min
    if(GeoLocTxAmountMax < objeto.geolocation.metadata.bytes.max):
        GeoLocTxAmountMax = objeto.geolocation.metadata.bytes.max
    if(GeoLocTxAmountMin > objeto.geolocation.metadata.bytes.min):
        GeoLocTxAmountMin = objeto.geolocation.metadata.bytes.min
    if(GeoLocVisitorsMax < objeto.geolocation.metadata.visitors.max):
        GeoLocVisitorsMax = objeto.geolocation.metadata.visitors.max
    if(GeoLocVisitorsMin > objeto.geolocation.metadata.visitors.min):
        GeoLocVisitorsMin = objeto.geolocation.metadata.visitors.min


    if(URLVisitorsMin > objeto.requests.metadata.visitors.min):
        URLVisitorsMin = objeto.requests.metadata.visitors.min
    if(URLTxAmountMin > objeto.requests.metadata.bytes.min):
        URLTxAmountMin = objeto.requests.metadata.bytes.min
    if(URLHitsMin > objeto.requests.metadata.hits.min):
        URLHitsMin = objeto.requests.metadata.hits.min

    if(VisitorsHitsMin > objeto.visitors.metadata.hits.min):
        VisitorsHitsMin = objeto.visitors.metadata.hits.min
    if(VisitorsVisitorsMin > objeto.visitors.metadata.visitors.min):
        VisitorsVisitorsMin = objeto.visitors.metadata.visitors.min
    if(VisitorsTxAmountMin > objeto.visitors.metadata.bytes.min):
        VisitorsTxAmountMin = objeto.visitors.metadata.bytes.min

    print("Teste para ver os valores máximos reais: ", URLVisitorsMax, URLHitsMax, URLTxAmountMax,
          )

    #GrandeDataURL = "".join(str(objeto.requests.metadata.visitors))
    printvariaveis()

def listarAtributos(objeto): # função que imprime os atributos do objeto
    atributos = dir(objeto)
    for atributo in atributos:
        valor = getattr(objeto, atributo)
        print(f"{atributo}: {valor}")
        if isinstance(valor, dict):
            listarAtributos(valor)

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


def trocaValoresJson(jsonDecod):
    jsonDecod.general.total_requests = TotalRequests
    jsonDecod.general.valid_requests = ValidRequests 
    jsonDecod.general.failed_requests = FailedRequests
    jsonDecod.general.unique_visitors = ExclusiveIPHits 
    jsonDecod.general.unique_referrers = Refferers 
    jsonDecod.general.unique_not_found = NotFound
    jsonDecod.general.generation_time = InitProcTime
    jsonDecod.general.unique_static_files = StaticFiles 
    jsonDecod.general.unique_visitors = UniqueVisitors
    jsonDecod.general.log_size = LogSize
    jsonDecod.general.unique_files = RequestedFiles 
    jsonDecod.general.bandwidth = TxAmount 

    jsonDecod.visitors.metadata.hits.count = HitsVisitor
    jsonDecod.visitors.metadata.visitors.count = VisitorsVisitor
    jsonDecod.visitors.metadata.bytes.count = TxAmountVisitor
    jsonDecod.visitors.metadata.data.unique = DataVisitor

    jsonDecod.requests.metadata.hits.count = HitsURL
    jsonDecod.requests.metadata.visitors.count = VisitorsURL
    jsonDecod.requests.metadata.bytes.count = TxAmountURL
    jsonDecod.requests.metadata.data.unique = DataURL

    jsonDecod.browsers.metadata.hits.count = BrowsersHits
    jsonDecod.browsers.metadata.visitors.count = BrowsersVisitors
    jsonDecod.browsers.metadata.data.unique = BrowsersData
    jsonDecod.browsers.metadata.bytes.count = BrowsersTxAmount

    jsonDecod.geolocation.metadata.hits.count = GeoLocHits
    jsonDecod.geolocation.metadata.visitors.count = GeoLocVisitors
    jsonDecod.geolocation.metadata.bytes.count = GeoLocTxAmount
    jsonDecod.geolocation.metadata.data.unique = GeolocData

    jsonDecod.hosts.metadata.hits.count = VisitorHostHits
    jsonDecod.hosts.metadata.visitors.count = VisitorHostVisitors
    jsonDecod.hosts.metadata.bytes.count = VisitorHostTxAmount
    jsonDecod.hosts.metadata.data.unique = VisitorHostData

    jsonDecod.not_found.metadata.hits.count = NotFoundHits
    jsonDecod.not_found.metadata.visitors.count = NotFoundVisitors
    jsonDecod.not_found.metadata.bytes.count = VisitorHostTxAmount
    jsonDecod.not_found.metadata.data.unique = VisitorHostData

    jsonDecod.os.metadata.hits.count = OperatingSysHits
    jsonDecod.os.metadata.visitors.count = OperatingSysVisitors
    jsonDecod.os.metadata.bytes.count = OperatingSysTxAmount
    jsonDecod.os.metadata.data.unique = VisitorHostData

    jsonDecod.referring_sites.metadata.hits.count = RefferSitesHits
    jsonDecod.referring_sites.metadata.visitors.count = RefferSitesVisitors
    jsonDecod.referring_sites.metadata.bytes.count = RefferSitesTxAmount
    jsonDecod.referring_sites.metadata.data.unique = RefferSitesData

    jsonDecod.static_requests.metadata.hits.count = StaticHits
    jsonDecod.static_requests.metadata.visitors.count = StaticVisitors
    jsonDecod.static_requests.metadata.bytes.count = StaticTxamount
    jsonDecod.static_requests.metadata.data.unique = StaticData

    jsonDecod.status_codes.metadata.hits.count = HttpStatCodesHits
    jsonDecod.status_codes.metadata.visitors.count = HttpStatCodesVisitors
    jsonDecod.status_codes.metadata.bytes.count = HttpStatCodesTxAmount
    jsonDecod.status_codes.metadata.data.unique = HttpStatCodesData

    jsonDecod.visit_time.metadata.hits.count = TimeDistrHits
    jsonDecod.visit_time.metadata.visitors.count = TimeDistrVisitors
    jsonDecod.visit_time.metadata.bytes.count = TimeDistrTxAmount
    jsonDecod.visit_time.metadata.data.unique = TimeDistrData

    # Troca valores o data, com o vetor gigante

    jsonDecod.browsers.data = DataBrowsers
    jsonDecod.geolocation.data = DataGeo
    jsonDecod.hosts.data = DataHosts
    jsonDecod.not_found.data = DataNotFound
    jsonDecod.os.data = DataOs
    jsonDecod.referring_sites.data = DataReferring
    jsonDecod.requests.data = DataRequests
    jsonDecod.static_requests.data = DataStaticRequests
    jsonDecod.status_codes.data = DataStatusCodes
    jsonDecod.visit_time.data = DataVisitTime
    jsonDecod.visitors.data = DataVisitors

    #print("BATATA",type(jsonDecod.requests.metadata.hits.max.real))
    #Inserindo os máximos e os mínimos
    jsonDecod.requests.metadata.hits.max = URLHitsMax
    jsonDecod.requests.metadata.hits.min = URLHitsMin
    jsonDecod.requests.metadata.bytes.max = URLTxAmountMax
    jsonDecod.requests.metadata.bytes.min = URLTxAmountMin
    jsonDecod.requests.metadata.visitors.max = URLVisitorsMax
    jsonDecod.requests.metadata.visitors.min = URLVisitorsMin
    
    jsonDecod.visitors.metadata.hits.max = VisitorsHitsMax
    jsonDecod.visitors.metadata.hits.min = VisitorsHitsMin
    jsonDecod.visitors.metadata.bytes.max = VisitorsTxAmountMax
    jsonDecod.visitors.metadata.bytes.min = VisitorsTxAmountMin
    jsonDecod.visitors.metadata.visitors.max = VisitorsVisitorsMax
    jsonDecod.visitors.metadata.visitors.max = VisitorsVisitorsMin

    jsonDecod.geolocation.metadata.hits.max = GeoLocHitsMax
    jsonDecod.geolocation.metadata.hits.min = GeoLocHitsMin
    jsonDecod.geolocation.metadata.visitors.max = GeoLocVisitorsMax
    jsonDecod.geolocation.metadata.visitors.min = GeoLocVisitorsMin
    jsonDecod.geolocation.metadata.bytes.max = GeoLocTxAmountMax
    jsonDecod.geolocation.metadata.bytes.min = GeoLocTxAmountMin

    jsonDecod.hosts.metadata.hits.max = VisitorHostIpHitsMax
    jsonDecod.hosts.metadata.hits.min = VisitorHostIpHitsMin
    jsonDecod.hosts.metadata.visitors.max = VisitorHostVisitorsMax
    jsonDecod.hosts.metadata.visitors.min = VisitorsHostVisitorsMin
    jsonDecod.hosts.metadata.bytes.max = VisitorsHostTxAmountMax
    jsonDecod.hosts.metadata.bytes.min = VisitorsHostTxAmountMin

    jsonDecod.not_found.metadata.hits.max = NotFoundHitsMax
    jsonDecod.not_found.metadata.hits.min = NotFoundHitsMin
    jsonDecod.not_found.metadata.visitors.max = NotFoundVisitorsMax
    jsonDecod.not_found.metadata.visitors.min = NotfoundVisitorsMin
    jsonDecod.not_found.metadata.bytes.max = NotFoundTxAmountMax
    jsonDecod.not_found.metadata.bytes.min = NotfoundTxAmountMin

    jsonDecod.os.metadata.hits.max = OperatingSysHitsMax
    jsonDecod.os.metadata.hits.min = OperatingSysHitsMin
    jsonDecod.os.metadata.visitors.max = OperatingSysVisitorsMax
    jsonDecod.os.metadata.visitors.min = OperatingSysVisitorsMin
    jsonDecod.os.metadata.bytes.max = OperatingSysTxAmountMax
    jsonDecod.os.metadata.bytes.min = OperatingSysTxAMountMin

    jsonDecod.referring_sites.metadata.hits.max = RefferSitesHitsMax
    jsonDecod.referring_sites.metadata.hits.min = RefferSitesHitsMin
    jsonDecod.referring_sites.metadata.visitors.max = RefferSitesVisitorsMax
    jsonDecod.referring_sites.metadata.visitors.min = RefferSitesVisitorsMin
    jsonDecod.referring_sites.metadata.bytes.max = RefferSitesTxAmountMax
    jsonDecod.referring_sites.metadata.bytes.min = RefferSitesTxAmountMin

    jsonDecod.static_requests.metadata.hits.max = StaticHitsMax
    jsonDecod.static_requests.metadata.hits.min = StaticHitsMin
    jsonDecod.static_requests.metadata.visitors.max = StaticVisitorsMax
    jsonDecod.static_requests.metadata.visitors.min = StaticVisitorsMin
    jsonDecod.static_requests.metadata.bytes.max = StaticTxAmountMax
    jsonDecod.static_requests.metadata.bytes.min = StaticTxAmountMin

    jsonDecod.status_codes.metadata.hits.max = HttpStatCodesHitsMax
    jsonDecod.status_codes.metadata.hits.min = HttpStatCodesHitsMin
    jsonDecod.status_codes.metadata.visitors.max = HttpStatCodesVisitorsMax
    jsonDecod.status_codes.metadata.visitors.min = HttpStatCodesVisitorsMin
    jsonDecod.status_codes.metadata.bytes.max = HttpStatCodesTxAmountMax
    jsonDecod.status_codes.metadata.bytes.min = HttpStatCodesTxAmountMin

    jsonDecod.visit_time.metadata.hits.max = TimeDistrHitsMax
    jsonDecod.visit_time.metadata.hits.min = TimeDistrHitsMin
    jsonDecod.visit_time.metadata.visitors.max = TimeDistrVisitorsMax
    jsonDecod.visit_time.metadata.visitors.min = TimeDistrVisitorsMin
    jsonDecod.visit_time.metadata.bytes.max = TimeDistrTxAmountMax
    jsonDecod.visit_time.metadata.bytes.min = TimeDistrTxAmountMin

    jsonDecod.browsers.metadata.hits.max = BrowsersHitsMax
    jsonDecod.browsers.metadata.hits.min = BrowsersHitsMin
    jsonDecod.browsers.metadata.visitors.max = BrowsersVisitorsMax
    jsonDecod.browsers.metadata.visitors.min = BrowsersVisitorsMin
    jsonDecod.browsers.metadata.bytes.max = BrowsersTxAmountMax
    jsonDecod.browsers.metadata.bytes.min = BrowsersTxAmountMin


    return jsonDecod

def pegaJsonHTMLtemplate(URL):
    print("Iniciando pegamento do html")
    request = requests.get(url = URL)
    soup = BeautifulSoup(request.text, "lxml")
    VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
    try:
        conteudo = VarJson[1].text # Pega o que tem dentro da tag.
        conteudo = conteudo.replace("var json_data=", "") # Tira o "var json_data=" e deixa só as chaves.
    except:
        conteudo = None
    jsonDecod = json.loads(conteudo)
    jsonDecod = transformaObjeto(jsonDecod)
    return jsonDecod

def trocaJson(URL, jsonReal):
    jsonReal = "var json_data=" + str(jsonReal)
    jsonAntigo = ""
    print("Iniciando trocação do json")
    request = requests.get(url = URL)
    soup = BeautifulSoup(request.text, "lxml")
    VarJson = soup.find_all("script", type="text/javascript") #Primeiro pegamos a tag
    jsonAntigo = VarJson[1] # pega o valor da tag que precisamos
    #print(jsonAntigo)
    #print(jsonReal)
    #soup = str(soup)
    #jsonAntigo = str(jsonAntigo)
    jsonAntigo.string = jsonReal # modificamos a string que fica dentro da tag (no caso o json)


    #print(jsonReal)
    #print(jsonAntigo)
    #soup = soup.replace(jsonAntigo, jsonReal)
    #if(teste != soup):
    #    print("Fez replace")
    #else:
    #    print("não achou o replace")
    #jsonAntigo.string = (jsonReal)
    #print(jsonAntigo)
    #print("O json antigo é: ", jsonAntigo)
    #print("O json novo é: var json_data=" + str(jsonTrocado) )
    #soup = str(soup)
    #jsonAntigo.replace_with(jsonReal)
    with open("ArquivoHTMLtrocado.html", "w", encoding="utf-8") as arquivo:
            arquivo.write(str(soup))


def transformaDicionario(jsonReal):
    if isinstance(jsonReal, dict):
        return {chave: transformaDicionario(valor) for chave, valor in jsonReal.items()}
    elif isinstance(jsonReal, list):
        return [transformaDicionario(elemento) for elemento in jsonReal]
    elif isinstance(jsonReal, SimpleNamespace):
        return transformaDicionario(vars(jsonReal))
    else:
        return jsonReal



#########################################################################################################

print("Iniciando decodificação e soma das variaveis do json para depois trocar no JSON.")
selectSQL()
URL = "exemplo.com/" # Template para nossos truques
resultado = selectSQL() # pega as tuplas json do SQL
for valor in (resultado): # cada resultado da iteração, um novo objeto é formado.
    try:
        jsonDecod = json.loads(str(valor))
        if (type(jsonDecod) != dict): # pega da base de dados SQL (todos os valores que temos até agora)
            continue
    except:
        print("O valor não pôde ser decodificado.")

    objeto = transformaObjeto(jsonDecod) # cria um unico objeto através de um unico json decodificado de um unico json
    somaValores(objeto)

printvariaveis() # soma os máximos
jsondecodificado = pegaJsonHTMLtemplate(URL) # depois que o json foi decodificado de acordo com um template json
jsonTrocado = trocaValoresJson(jsondecodificado) # pega esse json e troca os valores de acordo com a soma.
#listarAtributos(jsonTrocado) # isso dá print numa versão dicionário do objeto.
###
#Os outros atributos estão em metadata
print([atributo for atributo in dir(jsonTrocado.general) if not atributo.startswith('__')])
print([atributo for atributo in dir(jsonTrocado) if not atributo.startswith('__')])
print([atributo for atributo in dir(jsonTrocado.requests.data) if not atributo.startswith('__')])
#print([atributo for atributo in dir(jsonTrocado.requests.data.pop) if not atributo.startswith('__')])
#print(str(jsonTrocado.requests.metadata.visitors.max.real)) #só redescobrir o max e o min
#print(jsonTrocado.requests.metadata.visit)
#print("valor 1", jsonTrocado.requests.metadata.hits, "valor 2", jsonTrocado.requests.hits)
###
jsonReal = transformaDicionario(jsonTrocado) # depois transforma esse json objeto, num dicionário de novo.
print("Teste de inserção das variáveis para confirmar integridade:",
    #ExclusiveIPHits,
    #ValidRequests,
    #jsonReal["general"]["unique_visitors"],
    #jsonReal["general"]["valid_request"],
    #jsonReal["requests"]["metadata"]["visitors"]["max"]
    #jsonReal["requests"]["data"]
    )
jsonReal = json.dumps(jsonReal) # transforma o dicionário no json novamente, com os valores modificados.
trocaJson(URL, jsonReal)
print("Troca de json no html bem sucedida")
#print(jsonReal["general"])
# agora preciso reinserir no html esse json. só pegar o request, daí usar replace com o json que temos agora.
#trocaJson(URL, jsonTrocado)
