import pyshark
from collections import Counter
import pickle

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

def analise_ipv4(pacotes):
    src_ips = Counter()
    dst_ips = Counter()

    for packet in pacotes:
        if 'IP' in packet:
            src_ips[packet.ip.src] += 1
            dst_ips[packet.ip.dst] += 1

    total_ips = src_ips + dst_ips
    most_common_ips = total_ips.most_common(10)

    return most_common_ips

# Exemplo de uso:

# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_ipv4_lidos.pcap'
pacotes = capturar_pacotes('ipv4_traffic.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_ipv4(pacotes_carregados)

# Exibe resultados
for ip, count in resultado_analise:
    print(f"IP: {ip}, Contagem: {count}")
