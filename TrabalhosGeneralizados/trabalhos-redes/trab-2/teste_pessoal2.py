import pyshark
from collections import Counter

# Leia o arquivo .pcap
capture = pyshark.FileCapture('arp_traffic.pcap')

# Contador para IPs de origem e destino
src_ips = Counter()
dst_ips = Counter()

# Contar a frequência dos IPs de origem e destino
for packet in capture:
    print(packet)

