import pyshark

pcap_file = 'ipv4_traffic.pcap'
cap = pyshark.FileCapture(pcap_file) # Leio o pacote

for packet in cap: # Itero sobre pacote
    if 'IP' in packet: # Verifico se existe a chave IP dentro do dicionário packet (in funciona diferente em cada tipo de dado)
        ip_src = packet.ip.src
        ip_dst = packet.ip.dst
        #print(dir(packet))
        #packet.pretty_print()
        #packet.interface_captured()
        print(packet)
        
        print(f"Endereço IP de origem: {ip_src}, Endereço IP de destino: {ip_dst}")

cap.close()
