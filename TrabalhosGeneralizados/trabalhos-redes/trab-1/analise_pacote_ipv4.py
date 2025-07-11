import pyshark
from collections import Counter

# Leia o arquivo .pcap
capture = pyshark.FileCapture('ipv4_traffic.pcap')

# Contadores para IPs de origem e destino
src_ips = Counter()
dst_ips = Counter()

# Contar a frequência dos IPs de origem e destino
for packet in capture:
    if 'IP' in packet:
        src_ips[packet.ip.src] += 1
        dst_ips[packet.ip.dst] += 1

# Combine os contadores
total_ips = src_ips + dst_ips

# Obtenha os 10 IPs com maior tráfego
most_common_ips = total_ips.most_common(10)
ips, counts = zip(*most_common_ips)

print("Ips mais comuns:")
for ip, count in most_common_ips:
    print(f"IP: {ip}, Contagem: {count}")

# Contador para IPs de destino
dst_ips = Counter()

# Contar a frequência dos IPs de destino
for packet in capture: # O packet de rede contém tanto IP, quanto ipv6
    if 'IP' in packet:
        dst_ips[packet.ip.dst] += 1

# Obtenha os 10 IPs de destino mais comuns
most_common_dst_ips = dst_ips.most_common(10)

# Exiba os IPs de destino mais comuns
print("Destinos mais comuns:")
for ip, count in most_common_dst_ips:
    print(f"IP: {ip}, Pacotes: {count}")