import pyshark
from collections import Counter

def ler_e_analisar_pacotes_udp(file):
    # Lê pacotes de um arquivo PCAP e conta os diferentes valores de "Hop Limit", status dos checksums,
    # e contagem de portas de origem e destino UDP
    captura_arquivo = pyshark.FileCapture(file, display_filter='udp')
    hop_limits = Counter()
    checksums = {'verified': 0, 'unverified': 0}
    source_ports = Counter()
    destination_ports = Counter()

    for pacote in captura_arquivo:
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

            
    
    captura_arquivo.close()
    return hop_limits, checksums, source_ports, destination_ports

def imprimir_resultados(hop_limits, checksums, source_ports, destination_ports):
    print("Contagem de Hop Limits:")
    for hop_limit, count in hop_limits.items():
        print(f"Hop Limit: {hop_limit}, Count: {count}")
    
    print("\nContagem de Checksums:")
    print(f"Verificados: {checksums['verified']}")
    print(f"Não Verificados: {checksums['unverified']}")
    
    print("\nContagem de Portas de Origem (Source Ports):")
    for port, count in source_ports.items():
        print(f"Source Port: {port}, Count: {count}")
    
    print("\nContagem de Portas de Destino (Destination Ports):")
    for port, count in destination_ports.items():
        print(f"Destination Port: {port}, Count: {count}")

file = 'captura_udp.pcap'
hop_limits, checksums, source_ports, destination_ports = ler_e_analisar_pacotes_udp(file)
imprimir_resultados(hop_limits, checksums, source_ports, destination_ports)
