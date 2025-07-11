import pyshark

#Pacotes http capturados:
#['record', 'record_content_type', 'record_version', 'record_length', 'app_data', 'app_data_proto']
#['segment_data']
#['record', 'record_content_type', 'record_version', 'record_length', 'app_data', 'app_data_proto']
#['record', 'record_content_type', 'record_version', 'record_length', 'app_data', 'app_data_proto']

from collections import Counter

def capturar_pacotes_tls(file):
    # Captura pacotes TLS de um arquivo PCAP
    captura = pyshark.FileCapture(file, display_filter='tls')
    pacotes_tls = []

    for pacote in captura:
        try:
            # Verifica se o pacote TLS contém o campo "record content type"
            if hasattr(pacote.tls, 'record_content_type'):
                # Extrai informações relevantes do pacote TLS
                info_pacote = {
                    'timestamp': pacote.sniff_time,
                    'source_ip': pacote.ip.src,
                    'destination_ip': pacote.ip.dst,
                    'tls_version': pacote.tls.record_version,
                    'content_type': pacote.tls.record_content_type,
                    'application_data_protocol': pacote.tls.record_protocol if hasattr(pacote.tls, 'record_protocol') else None
                }
                pacotes_tls.append(info_pacote)
        except AttributeError:
            # Ignora pacotes que não possuem o campo TLS
            pass

    captura.close()
    return pacotes_tls

def contar_https(pacotes_tls):
    total_https = 0

    for pacote in pacotes_tls:
        if pacote['application_data_protocol'] and 'http' in pacote['application_data_protocol'].lower():
            total_https += 1

    return total_https

def contar_ips(pacotes_tls):
    source_ips = Counter()
    destination_ips = Counter()

    for pacote in pacotes_tls:
        source_ips[pacote['source_ip']] += 1
        destination_ips[pacote['destination_ip']] += 1

    return source_ips, destination_ips

def contar_content_type(pacotes_tls):
    content_types = Counter()

    for pacote in pacotes_tls:
        content_types[pacote['content_type']] += 1

    return content_types

# Captura pacotes TLS de um arquivo PCAP
file = 'captura_https.pcap'
pacotes_tls = capturar_pacotes_tls(file=file)

# Conta quantos pacotes TLS são HTTPS
total_https = contar_https(pacotes_tls)
print(f"Total de pacotes TLS que são HTTPS: {total_https}")

# Conta os IPs de origem e destino mais comuns
source_ips, destination_ips = contar_ips(pacotes_tls)
content_types = contar_content_type(pacotes_tls)

# Exibe os 5 IPs de origem mais comuns
print("\nTop 5 IPs de origem mais comuns:")
for ip, count in source_ips.most_common(5):
    print(f"{ip}: {count}")

# Exibe os 5 IPs de destino mais comuns
print("\nTop 5 IPs de destino mais comuns:")
for ip, count in destination_ips.most_common(5):
    print(f"{ip}: {count}")

print("\nOs content types e sua contagem: (23 = application layer)")
for content_type, count in content_types.most_common():
    print(f"{content_type}: {count}")