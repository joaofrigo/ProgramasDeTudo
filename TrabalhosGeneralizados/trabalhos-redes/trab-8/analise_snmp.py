import pyshark
from collections import Counter

def contar_informacoes_snmp(file):
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
    captura_arquivo = pyshark.FileCapture(file, display_filter='snmp')
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

    # Função para imprimir os 10 valores mais comuns formatados
    def print_top_10(counter, title):
        print(f"\n{title}:")
        for key, value in counter.most_common(10):
            print(f"  {key}: {value}")

    # Imprime os resultados formatados
    print_top_10(count_versions, "Versões SNMP")
    print_top_10(count_communities, "Comunidades SNMP")
    print_top_10(count_data, "Dados SNMP")
    print_top_10(count_request_ids, "Request IDs SNMP")
    print_top_10(count_error_statuses, "Error Statuses SNMP")
    print_top_10(count_error_indices, "Error Indices SNMP")
    print_top_10(count_variable_bindings, "Variable Bindings SNMP")
    print_top_10(count_names, "Nomes SNMP")
    print_top_10(count_endofmibview, "End of MIB View SNMP")
    print_top_10(count_responses_to, "Responses To SNMP")

contar_informacoes_snmp(file='snmp.pcap')
