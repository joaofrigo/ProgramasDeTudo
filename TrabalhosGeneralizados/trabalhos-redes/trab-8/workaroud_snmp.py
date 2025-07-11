import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path, display_filter='snmp')
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

def analise_snmp(pacotes):
    # Inicializa contadores
    count_versions = Counter()
    count_communities = Counter()
    count_data = Counter()
    count_request_ids = Counter()
    count_error_statuses = Counter()
    count_error_indices = Counter()
    count_variable_bindings = Counter()
    count_names = Counter()
    count_endofmibview = Counter()
    count_responses_to = Counter()

    # Lê pacotes de um arquivo PCAP e conta informações relevantes de pacotes SNMP
    captura_arquivo = pacotes
    print("Contagem de informações SNMP:")

    for pacote in captura_arquivo:
        snmp_layer = pacote.snmp

        # Verifica se os campos estão presentes antes de contar
        if hasattr(snmp_layer, 'version'):
            version = snmp_layer.version
            count_versions[version] += 1

        if hasattr(snmp_layer, 'community'):
            community = snmp_layer.community
            count_communities[community] += 1

        if hasattr(snmp_layer, 'data'):
            data = snmp_layer.data
            count_data[data] += 1

        if hasattr(snmp_layer, 'request_id'):
            request_id = snmp_layer.request_id
            count_request_ids[request_id] += 1

        if hasattr(snmp_layer, 'error_status'):
            error_status = snmp_layer.error_status
            count_error_statuses[error_status] += 1

        if hasattr(snmp_layer, 'error_index'):
            error_index = snmp_layer.error_index
            count_error_indices[error_index] += 1

        if hasattr(snmp_layer, 'variable_bindings'):
            variable_bindings = snmp_layer.variable_bindings
            count_variable_bindings[variable_bindings] += 1

        # get_field_by_showname returns None if the field is not present
        name = snmp_layer.get_field_by_showname("Object Name")
        if name:
            count_names[name] += 1

        endofmibview = snmp_layer.get_field_by_showname("endOfMibView")
        if endofmibview:
            count_endofmibview[endofmibview] += 1

        response_to = snmp_layer.get_field_by_showname("Response To")
        if response_to:
            count_responses_to[response_to] += 1

    
    return {
        "count_versions": count_versions.most_common(5),
        "count_communities": count_communities.most_common(5),
        "count_data": count_data.most_common(5),
        "count_request_ids": count_request_ids.most_common(5),
        "count_error_statuses": count_error_statuses.most_common(5),
        "count_error_indices": count_error_indices.most_common(5),
        "count_variable_bindings": count_variable_bindings.most_common(5),
        "count_names": count_names.most_common(5),
        "count_responses_to": count_responses_to.most_common(5)
    }


# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_snmp_lidos.pcap'
pacotes = capturar_pacotes('snmp.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_snmp(pacotes_carregados)

print("Top 5 SNMP Versions:")
for version, count in resultado_analise["count_versions"]:
    print(f"Version: {version}, Count: {count}")

print("\nTop 5 SNMP Communities:")
for community, count in resultado_analise["count_communities"]:
    print(f"Community: {community}, Count: {count}")

print("\nTop 5 SNMP Data Fields:")
for data, count in resultado_analise["count_data"]:
    print(f"Data: {data}, Count: {count}")

print("\nTop 5 SNMP Request IDs:")
for request_id, count in resultado_analise["count_request_ids"]:
    print(f"Request ID: {request_id}, Count: {count}")

print("\nTop 5 SNMP Error Statuses:")
for error_status, count in resultado_analise["count_error_statuses"]:
    print(f"Error Status: {error_status}, Count: {count}")

print("\nTop 5 SNMP Error Indices:")
for error_index, count in resultado_analise["count_error_indices"]:
    print(f"Error Index: {error_index}, Count: {count}")

print("\nTop 5 SNMP Variable Bindings:")
for variable_binding, count in resultado_analise["count_variable_bindings"]:
    print(f"Variable Binding: {variable_binding}, Count: {count}")

print("\nTop 5 SNMP Object Names:")
for name, count in resultado_analise["count_names"]:
    print(f"Object Name: {name}, Count: {count}")

print("\nTop 5 SNMP Responses To:")
for response_to, count in resultado_analise["count_responses_to"]:
    print(f"Response To: {response_to}, Count: {count}")



