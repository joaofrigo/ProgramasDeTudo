import pyshark

def ler_e_imprimir_mac_arp(file):
    # Lê pacotes de um arquivo PCAP e imprime os endereços MAC únicos
    captura_arquivo = pyshark.FileCapture(file, display_filter='arp')
    mac_addresses = set()  # Usar um set para evitar endereços MAC duplicados
    reply_mac_addresses = set()  # Usar um set para endereços MAC que responderam a ARP
    
    print("Endereços MAC capturados:")
    for pacote in captura_arquivo:
        try:
            # Extraindo endereços MAC da camada ARP
            src_mac_arp = pacote.arp.src_hw_mac
            dst_mac_arp = pacote.arp.dst_hw_mac
            mac_addresses.add(src_mac_arp)
            mac_addresses.add(dst_mac_arp)

            # Extraindo endereços MAC da camada Ethernet
            src_mac_eth = pacote.eth.src
            dst_mac_eth = pacote.eth.dst
            mac_addresses.add(src_mac_eth)
            mac_addresses.add(dst_mac_eth)

            # Verificar se o pacote é uma resposta ARP (opcode == 2)
            if pacote.arp.opcode == '2':
                reply_mac_addresses.add(src_mac_arp)
        except AttributeError:
            # Pular pacotes que não têm os campos esperados
            continue

    # Imprimir endereços MAC únicos
    for mac in mac_addresses:
        if mac == '00:00:00:00:00:00':
            print(f"{mac} (Endereço MAC de destino desconhecido em solicitação ARP)")
        else:
            print(mac)
    
    # Imprimir endereços MAC que responderam a ARP
    print("\nEndereços MAC que responderam a solicitações ARP:")
    for mac in reply_mac_addresses:
        print(mac)

file = 'captura_arp.pcap'

ler_e_imprimir_mac_arp(file)
