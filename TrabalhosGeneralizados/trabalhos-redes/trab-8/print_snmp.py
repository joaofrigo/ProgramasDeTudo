import pyshark

def ler_e_imprimir_pacotes_arquivo(file):
    # Lê pacotes de um arquivo PCAP e imprime os pacotes ARP
    captura_arquivo = pyshark.FileCapture(file, display_filter='snmp')
    print("Pacotes snmp capturados:")
    for pacote in captura_arquivo:
        #print(pacote.snmp.field_names)
        print(pacote)

ler_e_imprimir_pacotes_arquivo(file='snmp.pcap')