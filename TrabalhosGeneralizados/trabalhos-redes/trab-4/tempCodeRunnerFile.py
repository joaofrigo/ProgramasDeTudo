    # Lê pacotes de um arquivo PCAP e conta os diferentes valores de "Hop Limit", status dos checksums,
    # e contagem de portas de origem e destino UDP
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