from scapy.all import ARP, Ether, sendp
import pyshark
import time

def ler_e_imprimir_pacotes_arquivo(file):
    # Lê pacotes de um arquivo PCAP e imprime os pacotes ARP
    captura = pyshark.FileCapture(file, display_filter='arp')
    print("Pacotes ARP capturados:")
    for pacote in captura:
        print(pacote)

ler_e_imprimir_pacotes_arquivo(file='captura_arp.pcap')