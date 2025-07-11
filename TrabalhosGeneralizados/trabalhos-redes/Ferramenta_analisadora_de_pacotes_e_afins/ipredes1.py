import dpkt
import socket

def printPcap(pcap):
    for (ts,buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print('origem: ' + src + ' destino: ' + dst)
        except Exception as e:
            #não é ip
            pass

def main():
    with open('trabalho1.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        printPcap(pcap)

if __name__ == '__main__':
    main()
