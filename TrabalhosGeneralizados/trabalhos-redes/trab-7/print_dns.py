import pyshark

def ler_e_imprimir_pacotes_arquivo(file):
    # Lê pacotes de um arquivo PCAP e imprime os pacotes ARP
    captura_arquivo = pyshark.FileCapture(file, display_filter='dns')
    print("Pacotes dns capturados:")
    for pacote in captura_arquivo:
        print(pacote.dns.field_names)
        #print(pacote)

ler_e_imprimir_pacotes_arquivo(file='captura_dns.pcap')