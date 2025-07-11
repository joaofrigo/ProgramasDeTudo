import pyshark


def adquirir_pacotes():
    # Crie um objeto capturador de pacotes
    cap = pyshark.LiveCapture(interface='Ethernet', output_file='pacote_de_ethernet')
    cap2 = pyshark.LiveCapture(interface='Radmin VPN', output_file='pacote_de_VPN')
    cap3 =pyshark.LiveCapture(interface='Adapter for loopback traffic capture', output_file='pacote_de_loopback')

    # Inicie a captura
    cap.sniff(timeout=100)  # Capture por 10 segundos, por exemplo
    cap2.sniff(timeout=100)
    cap3.sniff(timeout=100)

    print("acabou")


adquirir_pacotes()