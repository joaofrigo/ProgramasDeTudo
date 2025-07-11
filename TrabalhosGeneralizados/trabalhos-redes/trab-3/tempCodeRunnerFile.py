import pyshark

def contar_informacoes_rip(file):
    # Inicializa contadores
    count_command_response = 0
    count_routes = 0

    # Lê pacotes de um arquivo PCAP e conta informações relevantes de pacotes RIP
    captura_arquivo = pyshark.FileCapture(file, display_filter='rip')
    print("Contagem de informações RIP:")

    for pacote in captura_arquivo:
        rip_layer = pacote.rip
        
        # Conta comandos RIP (Request ou Response)
        if rip_layer.command == '2':  # '2' representa Response
            count_command_response += 1
        
        # Conta número de rotas anunciadas
        count_routes += len(rip_layer.ip)

    # Imprime os resultados
    print(f"Comandos Response RIP (2): {count_command_response}")
    print(f"Número total de rotas anunciadas: {count_routes}")

contar_informacoes_rip(file='RIPv2_subnet_down.pcap')
