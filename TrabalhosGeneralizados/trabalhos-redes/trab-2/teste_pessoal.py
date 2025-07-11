import pyshark

# Defina a interface de rede que você deseja monitorar
interface = 'Ethernet'  # Substitua 'eth0' pela sua interface de rede

# Capture o tráfego na interface especificada e salve em um arquivo .pcap
capture = pyshark.LiveCapture(interface=interface, output_file='arp_traffic.pcap')

# Capture 10 pacotes
capture.sniff(packet_count=100)

print("Captura de pacotes concluída e salva em arp_traffic.pcap")
