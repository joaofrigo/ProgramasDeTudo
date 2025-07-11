import pyshark
from collections import Counter
import pickle
import os

def capturar_pacotes(file_path):
    capture = pyshark.FileCapture(file_path)
    pacotes = list(capture)  # Lê todos os pacotes do arquivo e armazena em uma lista
    capture.close()  # Fecha o FileCapture após ler todos os pacotes
    return pacotes

def salvar_pacotes_em_arquivo(pacotes, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(pacotes, f)

def carregar_pacotes_do_arquivo(file_path):
    with open(file_path, 'rb') as f:
        pacotes = pickle.load(f)
    return pacotes

def analise_ipv4_script(pacotes):
    src_ips = Counter()
    dst_ips = Counter()

    for packet in pacotes:
        if 'IP' in packet:
            src_ips[packet.ip.src] += 1
            dst_ips[packet.ip.dst] += 1

    # Obtém os 10 IPs de origem mais comuns
    most_common_src_ips = src_ips.most_common(10)

    # Obtém os 10 IPs de destino mais comuns
    most_common_dst_ips = dst_ips.most_common(10)

    return most_common_src_ips, most_common_dst_ips


def analise_ipv4():
    # Obtém o diretório atual do script
    script_dir = os.path.dirname(__file__)

    # Monta o caminho completo para o arquivo de pacotes
    file_path = os.path.join(script_dir, 'pacotes_ipv4_lidos.pcap')

    # Carrega os pacotes do arquivo
    pacotes_carregados = carregar_pacotes_do_arquivo(file_path)

    # Realiza a análise dos pacotes
    resultado_analise = analise_ipv4_script(pacotes_carregados)
    return resultado_analise

<<<<<<< HEAD
def analise_arp():
    mac_addresses = set()  # Usar um set para evitar endereços MAC duplicados
    reply_mac_addresses = set()  # Usar um set para endereços MAC que responderam a ARP
    mac_counter = Counter()  # Contador para a frequência dos endereços MAC
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_arp_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    for pacote in pacotes:
        try:
            # Extraindo endereços MAC da camada ARP
            src_mac_arp = pacote.arp.src_hw_mac
            dst_mac_arp = pacote.arp.dst_hw_mac
            mac_addresses.add(src_mac_arp)
            mac_addresses.add(dst_mac_arp)
            mac_counter.update([src_mac_arp, dst_mac_arp])

            # Extraindo endereços MAC da camada Ethernet
            src_mac_eth = pacote.eth.src
            dst_mac_eth = pacote.eth.dst
            mac_addresses.add(src_mac_eth)
            mac_addresses.add(dst_mac_eth)
            mac_counter.update([src_mac_eth, dst_mac_eth])

            # Verificar se o pacote é uma resposta ARP (opcode == 2)
            if pacote.arp.opcode == '2':
                reply_mac_addresses.add(src_mac_arp)
        except AttributeError:
            continue

    # Converter conjuntos para listas para facilitar o retorno
    mac_addresses_list = list(mac_addresses)
    reply_mac_addresses_list = list(reply_mac_addresses)
    
    # Obter os endereços MAC mais comuns
    common_mac_addresses = mac_counter.most_common()

    return {
        "unique_mac_addresses": mac_addresses_list,
        "reply_mac_addresses": reply_mac_addresses_list,
        "common_mac_addresses": common_mac_addresses,
        "mac_counter": mac_counter
    }

def analise_rip():
    # Inicializa contadores e estruturas de dados
    count_command_response = 0
    count_routes = 0
    count_v2_version = 0
    count_v1_version = 0
    next_hop_counter = Counter()

    # Lê pacotes de um arquivo PCAP e conta informações relevantes de pacotes RIP
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_rip_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    captura_arquivo = pacotes

    for pacote in captura_arquivo:
        rip_layer = pacote.rip
        
        # Conta comandos RIP (Request ou Response)
        if rip_layer.command == '2':  # '2' representa Response
            count_command_response += 1
        
        # Conta número de rotas anunciadas
        count_routes += len(rip_layer.ip)

        # Conta versão do RIP
        if rip_layer.version == '2':
            count_v2_version += 1
        elif rip_layer.version == '1':
            count_v1_version += 1
        
        # Conta Next Hops mais comuns
        if hasattr(rip_layer, 'next_hop'):
            next_hop_counter[rip_layer.next_hop] += 1
    
    # Obtém os 3 Next Hops mais comuns
    top3_next_hops = next_hop_counter.most_common(3)

    return {
        "count_command_response": count_command_response,
        "count_routes": count_routes,
        "count_v1_version": count_v1_version,
        "count_v2_version": count_v2_version,
        "top3_next_hops": top3_next_hops,
        "next_hop_counter": next_hop_counter
    }

def analise_udp():
    # Lê pacotes de um arquivo PCAP e conta os diferentes valores de "Hop Limit", status dos checksums,
    # e contagem de portas de origem e destino UDP
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_udp_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    captura_arquivo = pacotes
    hop_limits = Counter()
    checksums = {'verified': 0, 'unverified': 0}
    source_ports = Counter()
    destination_ports = Counter()

    for pacote in captura_arquivo:
        try:
            # Contagem de Hop Limits
            if "ipv6" in pacote:
                hop_limit = int(pacote['IPV6'].hlim)
                hop_limits[hop_limit] += 1
            
            # Contagem de Checksums
            checksum_status = pacote['UDP'].checksum_status
            if checksum_status == '2':  # Verificado
                checksums['unverified'] += 1
            else:
                checksums['verified'] += 1
            
            # Contagem de Portas de Origem e Destino
            source_port = int(pacote['UDP'].srcport)
            destination_port = int(pacote['UDP'].dstport)
            source_ports[source_port] += 1
            destination_ports[destination_port] += 1

        except AttributeError:
            continue

    return {
        "hop_limits": hop_limits,
        "checksums": checksums,
        "source_ports": source_ports,
        "destination_ports": destination_ports
    }

def analise_tcp():
    # Lê pacotes de um arquivo PCAP e conta os valores relevantes dos pacotes TCP
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_tcp_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    captura_arquivo = pacotes
    source_ports = Counter()
    destination_ports = Counter()
    flags_counter = Counter()
    checksums = {'verified': 0, 'unverified': 0}

    for pacote in captura_arquivo:
        try:
            # Contagem de Portas de Origem e Destino
            source_port = int(pacote['TCP'].srcport)
            destination_port = int(pacote['TCP'].dstport)
            source_ports[source_port] += 1
            destination_ports[destination_port] += 1

            # Contagem de Flags
            flags = pacote['TCP'].flags
            flags_counter[flags] += 1

            # Contagem de Checksums
            checksum_status = pacote['TCP'].checksum_status
            if checksum_status == '2':  # Verificado
                checksums['verified'] += 1
            else:
                checksums['unverified'] += 1

        except AttributeError:
            continue

    return {
        "source_ports": source_ports.most_common(5),
        "destination_ports": destination_ports.most_common(5),
        "flags_counter": flags_counter.most_common(5),
        "checksums": checksums
    }

def analise_http():
    # Lê pacotes de um arquivo PCAP e analisa os pacotes TLS para HTTPS
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_http_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    captura_arquivo = pacotes
    tls_versions = Counter()
    content_types = Counter()
    application_protocols = Counter()

    pacotes_tls = []

    for pacote in captura_arquivo:
        try:
            # Verifica se o pacote TLS contém o campo "record content type"
            if hasattr(pacote.tls, 'record_content_type'):
                # Extrai informações relevantes do pacote TLS
                info_pacote = {
                    'timestamp': pacote.sniff_time,
                    'source_ip': pacote.ip.src,
                    'destination_ip': pacote.ip.dst,
                    'tls_version': pacote.tls.record_version,
                    'content_type': pacote.tls.record_content_type,
                    'application_data_protocol': pacote.tls.record_protocol if hasattr(pacote.tls, 'record_protocol') else None
                }

                # Verifica se o protocolo de dados da aplicação é HTTP
                if info_pacote['application_data_protocol'] == 'http':
                    pacotes_tls.append(info_pacote)
                
                # Contagem das versões TLS
                tls_versions[pacote.tls.record_version] += 1
                
                # Contagem dos tipos de conteúdo
                content_types[pacote.tls.record_content_type] += 1

                # Contagem dos protocolos de dados da aplicação
                if info_pacote['application_data_protocol']:
                    application_protocols[info_pacote['application_data_protocol']] += 1

        except AttributeError:
            # Ignora pacotes que não possuem o campo TLS
            pass

    return {
        "pacotes_tls": pacotes_tls,
        "tls_versions": tls_versions.most_common(5),
        "content_types": content_types.most_common(5),
    }

def analise_dns():
    # Abrir o arquivo PCAP para capturar os pacotes DNS
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_dns_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
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

def analise_snmp():
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
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'pacotes_snmp_lidos.pcap')
    pacotes = carregar_pacotes_do_arquivo(file_path)
    print("Contagem de informações SNMP:")

    for pacote in pacotes:
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


=======
>>>>>>> 05e784f4c7a1d6b569f4ae427e976d1034f1cb37
# Exibe resultados
#for ip, count in resultado_analise:
#    print(f"IP: {ip}, Contagem: {count}")
