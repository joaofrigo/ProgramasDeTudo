import os
import pyshark
import time

def configurar_quagga():
    # Configurar o Quagga para enviar pacotes RIP
    quagga_daemons_config = """
zebra=yes
ripd=yes
    """
    
    quagga_ripd_config = """
router rip
 network eth0
 redistribute connected
    """

    # Escrever a configuração dos daemons
    with open('/etc/quagga/daemons', 'w') as daemons_file:
        daemons_file.write(quagga_daemons_config)
    
    # Escrever a configuração do RIP
    with open('/etc/quagga/ripd.conf', 'w') as ripd_conf_file:
        ripd_conf_file.write(quagga_ripd_config)

    # Reiniciar o serviço Quagga
    os.system('sudo service quagga restart')

def capturar_rip(interface):
    captura = pyshark.LiveCapture(interface=interface, display_filter='rip')
    
    print("Capturando pacotes RIP...")
    for pacote in captura.sniff_continuously():
        try:
            print(f"\nPacote #{pacote.number}:")
            print(f"Time: {pacote.sniff_time}")
            print(f"Source IP: {pacote.ip.src}")
            print(f"Destination IP: {pacote.ip.dst}")
            print(f"Command: {pacote.rip.cmd}")
            print(f"Version: {pacote.rip.version}")
            print("Routes:")
            for i in range(int(pacote.rip.route_count)):
                route = pacote.rip.get_field(f"rip.entry_{i}")
                print(f"  Address: {route.address}, Metric: {route.metric}, Next Hop: {route.nexthop}")
        except AttributeError:
            continue

    # Configurar Quagga para gerar pacotes RIP
    configurar_quagga()
    
    # Aguarde alguns segundos para garantir que o Quagga esteja configurado e enviando pacotes RIP
    time.sleep(10)
    
    # Substitua 'eth0' pela interface de rede apropriada
    interface = 'eth0'
    
    # Capturar pacotes RIP
    capturar_rip(interface)
