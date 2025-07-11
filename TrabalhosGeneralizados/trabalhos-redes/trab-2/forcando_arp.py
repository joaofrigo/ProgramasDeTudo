from scapy.all import ARP, Ether, sendp
import pyshark
import time

def enviar_arp_broadcast(interface, ip_rede):
    # Cria o pacote ARP
    arp = ARP(pdst=ip_rede)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    pacote = ether / arp

    # Envia o pacote ARP
    print(f"Enviando ARP broadcast para {ip_rede} na interface {interface}")
    sendp(pacote, iface=interface, verbose=False)

def capturar_pacotes(interface, timeout, output_file):
    # Captura pacotes na interface especificada por um tempo determinado
    print(f"Iniciando captura de pacotes na interface {interface} por {timeout} segundos")
    captura = pyshark.LiveCapture(interface=interface, output_file=output_file)
    captura.sniff(timeout=timeout)

def ler_e_imprimir_pacotes_arquivo(file):
    # Lê pacotes de um arquivo PCAP e imprime os pacotes ARP
    captura_arquivo = pyshark.FileCapture(file, display_filter='arp')
    print("Pacotes ARP capturados:")
    for pacote in captura_arquivo:
        print(pacote)

# Exemplo de uso
interface = "Ethernet"  # Substitua pelo GUID correto da sua interface de rede
ip_rede = "192.168.100.255"

# Envia um ARP broadcast para o endereço de broadcast da rede
enviar_arp_broadcast(interface, ip_rede)

# Espera um pouco antes de iniciar a captura para garantir que o pacote ARP seja enviado
#time.sleep(2)
output_file = 'captura_arp.pcap'
timeout = 180
# Captura pacotes ARP
#capturar_pacotes(interface, timeout, output_file)
ler_e_imprimir_pacotes_arquivo(output_file)
