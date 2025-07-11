import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path, display_filter='tcp')
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

def analise_tcp(pacotes):
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

    return {
        "source_ports": source_ports.most_common(5),
        "destination_ports": destination_ports.most_common(5),
        "flags_counter": flags_counter.most_common(5),
        "checksums": checksums
    }


# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_tcp_lidos.pcap'
pacotes = capturar_pacotes('captura_tcp.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_tcp(pacotes_carregados)


print("Contagem de Portas de Origem (Source Ports):")
for port, count in resultado_analise["source_ports"]:
    print(f"Source Port: {port}, Count: {count}")

print("\nContagem de Portas de Destino (Destination Ports):")
for port, count in resultado_analise["destination_ports"]:
    print(f"Destination Port: {port}, Count: {count}")

print("\nContagem de Flags:")
for flag, count in resultado_analise["flags_counter"]:
    print(f"Flags: {flag}, Count: {count}")

print("\nContagem de Checksums:")
print(f"Verificados: {resultado_analise['checksums']['verified']}")
print(f"Não Verificados: {resultado_analise['checksums']['unverified']}")