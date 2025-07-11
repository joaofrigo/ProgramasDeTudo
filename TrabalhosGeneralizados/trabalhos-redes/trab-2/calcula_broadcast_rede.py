import netifaces
import ipaddress

def listar_interfaces_detalhadas():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        print(f"Interface: {interface}")
        addrs = netifaces.ifaddresses(interface)
        for addr_family, addr_info in addrs.items():
            if addr_family == netifaces.AF_INET:
                for info in addr_info:
                    ip = info.get('addr', 'N/A')
                    netmask = info.get('netmask', 'N/A')
                    broadcast = info.get('broadcast', 'N/A')
                    print(f"  IP: {ip}")
                    print(f"  Netmask: {netmask}")
                    print(f"  Broadcast: {broadcast}")
        print()

def obter_endereco_rede(interface):
    try:
        # Obtém informações sobre a interface de rede especificada
        addrs = netifaces.ifaddresses(interface)

        # Obtém o endereço IP e a máscara de rede da interface
        ip_info = addrs[netifaces.AF_INET][0]
        ip_addr = ip_info['addr']
        netmask = ip_info['netmask']

        # Calcula o endereço de rede usando ipaddress
        rede = ipaddress.IPv4Network(f'{ip_addr}/{netmask}', strict=False)
        endereco_rede = rede.network_address

        return endereco_rede, rede.prefixlen
    except (ValueError, KeyError) as e:
        return f"Erro: {e}", None

def calcular_broadcast(endereco_rede, prefixlen):
    try:
        # Cria um objeto de rede a partir do endereço e prefixo fornecidos
        rede = ipaddress.ip_network(f'{endereco_rede}/{prefixlen}', strict=False)
        
        # Calcula o endereço de broadcast da rede
        endereco_broadcast = rede.broadcast_address
        
        return endereco_broadcast
    except ValueError as e:
        return f"Erro: {e}"

# Lista todas as interfaces de rede com detalhes
listar_interfaces_detalhadas()

# Exemplo de uso
interface = '{E33437A0-B1DB-4191-BA58-65D1E789E2F9}'  # Substitua pelo GUID correto da sua interface de rede
endereco_rede, prefixlen = obter_endereco_rede(interface)
if prefixlen is not None:
    endereco_broadcast = calcular_broadcast(endereco_rede, prefixlen)
    print(f"O endereço de rede para a interface {interface} é: {endereco_rede}/{prefixlen}")
    print(f"O endereço de broadcast para a rede {endereco_rede}/{prefixlen} é: {endereco_broadcast}")
else:
    print(endereco_rede)
