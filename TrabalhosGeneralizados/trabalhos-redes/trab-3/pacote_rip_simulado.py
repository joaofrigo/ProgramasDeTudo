from scapy.all import *

class RIPEntry(Packet):
    name = "RIP Entry"
    fields_desc = [
        ShortField("AFI", 2),
        ShortField("RouteTag", 0),
        IPField("IPAddress", "0.0.0.0"),
        IPField("Netmask", "255.255.255.0"),
        IPField("Nexthop", "0.0.0.0"),
        IntField("Metric", 1)
    ]

class RIP(Packet):
    name = "RIP Header"
    fields_desc = [
        ByteField("cmd", 2),
        ByteField("version", 2),
        ShortField("zero", 0)
    ]

def enviar_pacote_rip(source_ip, dest_ip):
    # Construir pacotes RIP
    rip_header = RIP()
    rip_entry1 = RIPEntry(IPAddress="192.168.1.0", Metric=1)
    rip_entry2 = RIPEntry(IPAddress="10.0.0.0", Metric=2)

    rip_packet = (
        Ether(dst="ff:ff:ff:ff:ff:ff") /
        IP(src=source_ip, dst=dest_ip) /
        UDP(sport=520, dport=520) /
        rip_header /
        rip_entry1 /
        rip_entry2
    )

    # Enviar pacote RIP
    sendp(rip_packet, iface="Ethernet")  # Substitua 'Ethernet' pela interface de rede adequada

if __name__ == "__main__":
    # Substitua pelos IPs de origem e destino desejados
    source_ip = "192.168.1.1"
    dest_ip = "224.0.0.9"  # Endereço multicast para RIP

    # Enviar pacote RIP
    enviar_pacote_rip(source_ip, dest_ip)
