import pyshark

def ler_e_imprimir_pacotes_arquivo(file):
    # Lê pacotes de um arquivo PCAP e imprime os pacotes ARP
    captura_arquivo = pyshark.FileCapture(file, display_filter='rip')
    print("Pacotes UDP capturados:")
    for pacote in captura_arquivo:
        print(pacote.rip.field_names)
        #print(pacote)

ler_e_imprimir_pacotes_arquivo(file='RIPv2_subnet_down.pcap')