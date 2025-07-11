import pyshark
from collections import Counter

def ler_e_imprimir_pacotes_arquivo(pacotes):
    # Lê pacotes de um arquivo PCAP e conta os valores relevantes dos pacotes TCP
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

    captura_arquivo.close()
    return {
        "source_ports": source_ports,
        "destination_ports": destination_ports,
        "flags_counter": flags_counter,
        "checksums": checksums
    }

ler_e_imprimir_pacotes_arquivo(file='captura_tcp.pcap')