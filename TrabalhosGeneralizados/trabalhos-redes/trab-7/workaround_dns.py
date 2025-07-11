import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path, display_filter='dns')
    pacotes = list(capture)  # Lê todos os pacotes do arquivo e armazena em uma lista
    capture.close()  # Fecha o FileCapture após ler todos os pacotes
    print("terminando em capturar pacotes")
    return pacotes

def salvar_pacotes_em_arquivo(pacotes, file_path):
    print("entrando em salvar pacotes")
    with open(file_path, 'wb') as f:
        pickle.dump(pacotes, f)
    print("terminando em salvar pacotes")

def carregar_pacotes_do_arquivo(file_path):
    with open(file_path, 'rb') as f:
        pacotes = pickle.load(f)
    return pacotes

def analise_http(pacotes):
    # Abrir o arquivo PCAP para capturar os pacotes DNS
    captura = pacotes

    # Inicializar contadores
    query_counts = Counter()
    answer_counts = Counter()
    authority_counts = Counter()
    additional_counts = Counter()
    query_names = Counter()
    response_names = Counter()
    query_types = Counter()
    response_types = Counter()
    response_codes = Counter()

    # Iterar sobre os pacotes capturados
    for pacote in captura:
        if hasattr(pacote, 'dns'):
            # Contar informações principais
            query_counts[int(pacote.dns.count_queries)] += 1
            answer_counts[int(pacote.dns.count_answers)] += 1
            authority_counts[int(pacote.dns.count_auth_rr)] += 1
            additional_counts[int(pacote.dns.count_add_rr)] += 1

            # Contar nomes de consulta e resposta
            if hasattr(pacote.dns, 'qry_name'):
                query_names[pacote.dns.qry_name.lower()] += 1
            if hasattr(pacote.dns, 'resp_name'):
                response_names[pacote.dns.resp_name.lower()] += 1

            # Contar tipos de consulta e resposta
            if hasattr(pacote.dns, 'qry_type'):
                query_types[pacote.dns.qry_type] += 1
            if hasattr(pacote.dns, 'resp_type'):
                response_types[pacote.dns.resp_type] += 1

            # Contar códigos de resposta
            response_codes[pacote.dns.flags_opcode] += 1

    # Retornar contadores com as informações coletadas
    return {
        'query_counts': query_counts.most_common(5),
        'answer_counts': answer_counts.most_common(5),
        'authority_counts': authority_counts.most_common(5),
        'additional_counts': additional_counts.most_common(5),
        'query_names': query_names.most_common(5),
        'response_names': response_names.most_common(5),
        'query_types': query_types.most_common(5),
        'response_types': response_types.most_common(5),
        'response_codes': response_codes.most_common(5)
    }


# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_dns_lidos.pcap'
pacotes = capturar_pacotes('captura_dns.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_http(pacotes_carregados)

print("\nContagem de Consultas DNS:")
for query_count, count in resultado_analise['query_counts']:
    print(f"Consultas: {query_count}, Count: {count}")

print("\nContagem de Respostas DNS:")
for answer_count, count in resultado_analise['answer_counts']:
    print(f"Respostas: {answer_count}, Count: {count}")

print("\nContagem de Autoridades DNS:")
for authority_count, count in resultado_analise['authority_counts']:
    print(f"Autoridades: {authority_count}, Count: {count}")

print("\nContagem de Adicionais DNS:")
for additional_count, count in resultado_analise['additional_counts']:
    print(f"Adicionais: {additional_count}, Count: {count}")

print("\nContagem de Nomes de Consulta DNS:")
for query_name, count in resultado_analise['query_names']:
    print(f"Nome de Consulta: {query_name}, Count: {count}")

print("\nContagem de Nomes de Resposta DNS:")
for response_name, count in resultado_analise['response_names']:
    print(f"Nome de Resposta: {response_name}, Count: {count}")

print("\nContagem de Tipos de Consulta DNS:")
for query_type, count in resultado_analise['query_types']:
    print(f"Tipo de Consulta: {query_type}, Count: {count}")

print("\nContagem de Tipos de Resposta DNS:")
for response_type, count in resultado_analise['response_types']:
    print(f"Tipo de Resposta: {response_type}, Count: {count}")

print("\nContagem de Códigos de Resposta DNS:")
for response_code, count in resultado_analise['response_codes']:
    print(f"Código de Resposta: {response_code}, Count: {count}")



