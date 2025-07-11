import pyshark

def capturar_pacotes(interface, timeout, output_file):
    # Captura pacotes na interface especificada por um tempo determinado
    print(f"Iniciando captura de pacotes na interface {interface} por {timeout} segundos")
    captura = pyshark.LiveCapture(interface=interface, output_file=output_file)
    captura.sniff(timeout=timeout)


interface = 'Ethernet'
timeout = 15
output_file = 'captura_snmp.pcap'
capturar_pacotes(interface, timeout, output_file)
print("Pacotes snmp capturados em:", output_file)