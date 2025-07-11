import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path, display_filter='arp')
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

def analise_arp(pacotes):
    mac_addresses = set()  # Usar um set para evitar endereços MAC duplicados
    reply_mac_addresses = set()  # Usar um set para endereços MAC que responderam a ARP
    mac_counter = Counter()  # Contador para a frequência dos endereços MAC
    
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


# Exemplo de uso:

# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_arp_lidos.pcap'
#pacotes = capturar_pacotes('captura_arp.pcap')
#salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_arp(pacotes_carregados)

print("Endereços MAC únicos capturados:")
for mac in resultado_analise["unique_mac_addresses"]:
    print(mac)

print("\nEndereços MAC que responderam a solicitações ARP:")
for mac in resultado_analise["reply_mac_addresses"]:
    print(mac)

print("\nEndereços MAC mais comuns:")
for mac, count in resultado_analise["common_mac_addresses"]:
    print(f"{mac}: {count} vezes")

