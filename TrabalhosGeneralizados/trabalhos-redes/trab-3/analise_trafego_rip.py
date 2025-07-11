import pyshark
from collections import Counter

def contar_informacoes_rip(file):
    # Inicializa contadores e estruturas de dados
    count_command_response = 0
    count_routes = 0
    count_v2_version = 0
    count_v1_version = 0
    next_hop_counter = Counter()

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

        # Conta versão do RIP
        if rip_layer.version == '2':
            count_v2_version += 1
        elif rip_layer.version == '1':
            count_v1_version += 1
        
        # Conta Next Hops mais comuns
        if hasattr(rip_layer, 'next_hop'):
            next_hop_counter[rip_layer.next_hop] += 1
    
    # Obtém os 3 Next Hops mais comuns
    top3_next_hops = next_hop_counter.most_common(3)

    # Imprime os resultados
    print(f"Comandos Response RIP (2): {count_command_response}")
    print(f"Número total de rotas anunciadas: {count_routes}")
    print(f"Número de pacotes RIP versão 1: {count_v1_version}")
    print(f"Número de pacotes RIP versão 2: {count_v2_version}")
    print("\nTop 3 Next Hops mais comuns:")
    for i, (next_hop, count) in enumerate(top3_next_hops, start=1):
        print(f"Posição {i}: Next Hop {next_hop} com {count} ocorrências")

contar_informacoes_rip(file='RIPv2_subnet_down.pcap')
