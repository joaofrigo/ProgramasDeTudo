import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path, display_filter='udp')
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

def analise_udp(pacotes):
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


# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_udp_lidos.pcap'
pacotes = capturar_pacotes('captura_udp.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_udp(pacotes_carregados)

print("Contagem de Hop Limits:")
for hop_limit, count in resultado_analise["hop_limits"].items():
    print(f"Hop Limit: {hop_limit}, Count: {count}")

print("\nContagem de Checksums:")
print(f"Verificados: {resultado_analise['checksums']['verified']}")
print(f"Não Verificados: {resultado_analise['checksums']['unverified']}")

print("\nContagem de Portas de Origem (Source Ports):")
for port, count in resultado_analise["source_ports"].items():
    print(f"Source Port: {port}, Count: {count}")

print("\nContagem de Portas de Destino (Destination Ports):")
for port, count in resultado_analise["destination_ports"].items():
    print(f"Destination Port: {port}, Count: {count}")

