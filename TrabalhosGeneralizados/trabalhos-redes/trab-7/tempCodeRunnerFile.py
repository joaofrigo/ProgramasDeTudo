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