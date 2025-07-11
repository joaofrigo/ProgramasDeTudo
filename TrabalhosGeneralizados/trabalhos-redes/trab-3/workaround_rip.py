import pyshark
from collections import Counter
import pickle

def capturar_pacotes(file_path):
    print("entrando em capturar pacotes")
    capture = pyshark.FileCapture(file_path)
    pacotes = list(capture)  # Lê todos os pacotes do arquivo e armazena em uma lista
    capture.close()  # Fecha o FileCapture após ler todos os pacotes
    print("terminando em capturar pacotes")
    return pacotes

def salvar_pacotes_em_arquivo(pacotes, file_path):
    print("entrando em salvar pacotes")
    with open(file_path, 'wb') as f:
        pickle.dump(pacotes, f)
    print("terminando em salvar pacotes")

def carregar_pacotes_do_arquivo(file_path):
    with open(file_path, 'rb') as f:
        pacotes = pickle.load(f)
    return pacotes

def analise_rip(pacotes):
    # Inicializa contadores e estruturas de dados
    count_command_response = 0
    count_routes = 0
    count_v2_version = 0
    count_v1_version = 0
    next_hop_counter = Counter()

    # Lê pacotes de um arquivo PCAP e conta informações relevantes de pacotes RIP
    captura_arquivo = pacotes

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

    return {
        "count_command_response": count_command_response,
        "count_routes": count_routes,
        "count_v1_version": count_v1_version,
        "count_v2_version": count_v2_version,
        "top3_next_hops": top3_next_hops,
        "next_hop_counter": next_hop_counter
    }


# Captura e salva os pacotes em um arquivo
file_path = 'pacotes_rip_lidos.pcap'
pacotes = capturar_pacotes('RIPv2_subnet_down.pcap')
salvar_pacotes_em_arquivo(pacotes, file_path)

# Carrega os pacotes do arquivo e realiza a análise
pacotes_carregados = carregar_pacotes_do_arquivo(file_path)
resultado_analise = analise_rip(pacotes_carregados)

print(f"Comandos Response RIP (2): {resultado_analise['count_command_response']}")
print(f"Número total de rotas anunciadas: {resultado_analise['count_routes']}")
print(f"Número de pacotes RIP versão 1: {resultado_analise['count_v1_version']}")
print(f"Número de pacotes RIP versão 2: {resultado_analise['count_v2_version']}")
print("\nTop 3 Next Hops mais comuns:")
for i, (next_hop, count) in enumerate(resultado_analise['top3_next_hops'], start=1):
    print(f"Posição {i}: Next Hop {next_hop} com {count} ocorrências")
