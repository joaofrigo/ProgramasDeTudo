from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import pyshark
<<<<<<< HEAD
import matplotlib
=======
>>>>>>> 05e784f4c7a1d6b569f4ae427e976d1034f1cb37
import matplotlib.pyplot as plt
import plotly.io as pio
import base64
from .analises_e_valores import *
<<<<<<< HEAD
matplotlib.use('Agg')  # Adicione esta linha para usar o backend 'Agg'
=======
import asyncio
>>>>>>> 05e784f4c7a1d6b569f4ae427e976d1034f1cb37
from concurrent.futures import ThreadPoolExecutor

def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")


def cria_grafico_dinamico(categorias, valores, titulo='Gráfico de Barras', cor='blue', largura=6, altura=6):
    # Verificar se o número de categorias corresponde ao número de valores
    if len(categorias) != len(valores):
        raise ValueError("O número de categorias deve ser igual ao número de valores.")
    
    # Criando o gráfico de barras dinâmico
    plt.figure(figsize=(largura, altura))
    plt.bar(categorias, valores, color=cor)
    plt.xlabel('Nomes')
    plt.ylabel('Valores')
    plt.title(titulo)

    # Salvando o gráfico como imagem em base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Fechando a figura para liberar memória
    plt.close()
<<<<<<< HEAD
=======

    return image_base64

def charts_view(request):
    categorias = ['bobalhão', 'boboca', 'bobinho']
    valores = [10, 20, 15]
    titulo = 'Exemplo de Gráfico de Barras'
    cor = 'green'
    image_base64 = cria_grafico_dinamico(categorias, valores, titulo, cor, largura=8, altura=4)

    ip_comum, ip_destino_comum = analise_ipv4()
    
    # Criar listas para categorias e valores
    categorias_ips = []
    valores_ips = []

    # Adicionar categorias e valores para ip_comum
    for ip, count in ip_comum:
        categorias_ips.append(f'IP src: {ip}')
        valores_ips.append(count)

    # Adicionar categorias e valores para ip_destino_comum
    for ip, count in ip_destino_comum:
        categorias_ips.append(f'IP dst: {ip}')
        valores_ips.append(count)

    titulo_ips = 'ips mais comuns do ipv4'
    cor_ips = 'purple'
    image_trabalho_1_ips = cria_grafico_dinamico(categorias_ips, valores_ips, titulo_ips, cor_ips, largura=18, altura=6)

    # Incluir os gráficos no contexto
    context = {
        'grafico_base64': image_base64,
        'trabalho_1_ips': image_trabalho_1_ips
    }
>>>>>>> 05e784f4c7a1d6b569f4ae427e976d1034f1cb37

    return image_base64

<<<<<<< HEAD
def charts_view(request):
    categorias = ['bobalhão', 'boboca', 'bobinho']
    valores = [10, 20, 15]
    titulo = 'Exemplo de Gráfico de Barras'
    cor = 'green'
    image_base64 = cria_grafico_dinamico(categorias, valores, titulo, cor, largura=8, altura=4)

    ip_comum, ip_destino_comum = analise_ipv4() #######################################################################
=======
"""
def charts(request):

    #########################################################################################################

    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 3, 4, 5, 6]
    trace = go.Scatter(x=x_data, y=y_data, mode='markers')
    layout = go.Layout(title='Teste Inicial', xaxis=dict(title='Eixo X'), yaxis=dict(title='Eixo Y'))
    fig = go.Figure(data=[trace], layout=layout)
    primeiro_grafico = go.Figure.to_html(fig, include_plotlyjs=False)

    #########################################################################################################

    ips = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
    frequencia = [100, 150, 200, 250]
    sorted_ips = [ip for _, ip in sorted(zip(frequencia, ips), reverse=True)]
    sorted_frequencia = sorted(frequencia, reverse=True)
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=[sorted_frequencia],
        x=sorted_ips,
        y=['Frequencia'],
        colorscale='Viridis'))
    segundo_grafico = go.Figure.to_html(fig_heatmap, include_plotlyjs=False)

    # Renderiza ambos os gráficos na página
    context = {'primeiro_grafico': primeiro_grafico, 'segundo_grafico': segundo_grafico}
    leitor_ip()
    return render(request, 'charts.html', context)
"""


def leitor_ip():
    pcap_file = 'Pacote_de_rede.pcap'
    cap = pyshark.FileCapture(pcap_file) # Leio o pacote

    for packet in cap: # Itero sobre pacote
        if 'IP' in packet: # Verifico se existe a chave IP dentro do dicionário packet (in funciona diferente em cada tipo de dado)
            ip_src = packet.ip.src
            ip_dst = packet.ip.dst
            #print(dir(packet))
            #packet.pretty_print()
            #packet.interface_captured()
>>>>>>> 05e784f4c7a1d6b569f4ae427e976d1034f1cb37
    
    # Criar listas para categorias e valores
    categorias_ips = []
    valores_ips = []

    # Adicionar categorias e valores para ip_comum
    for ip, count in ip_comum:
        categorias_ips.append(f'IP src: {ip}')
        valores_ips.append(count)

    # Adicionar categorias e valores para ip_destino_comum
    for ip, count in ip_destino_comum:
        categorias_ips.append(f'IP dst: {ip}')
        valores_ips.append(count)

    titulo_ips = 'ips mais comuns do ipv4'
    cor_ips = 'purple'
    image_trabalho_1_ips = cria_grafico_dinamico(categorias_ips, valores_ips, titulo_ips, cor_ips, largura=18, altura=6)

    mac_data = analise_arp() #######################################################################

   # Criar gráficos para cada conjunto de dados
    image_unique = cria_grafico_dinamico(
        categorias=[str(i) for i in range(len(mac_data["unique_mac_addresses"]))],
        valores=mac_data["unique_mac_addresses"],
        titulo='Unique MAC Addresses',
        cor='blue',
        largura=13,
        altura=4
    )

    image_reply = cria_grafico_dinamico(
        categorias=[str(i) for i in range(len(mac_data["reply_mac_addresses"]))],
        valores=mac_data["reply_mac_addresses"],
        titulo='Reply MAC Addresses',
        cor='green',
        largura=8,
        altura=4
    )

    # Extraindo categorias e valores de common_mac_addresses (lista de tuplas)
    common_mac_addresses = mac_data["common_mac_addresses"]
    categorias_common = [mac for mac, _ in common_mac_addresses]
    valores_common = [count for _, count in common_mac_addresses]

    image_common = cria_grafico_dinamico(
        categorias=categorias_common,
        valores=valores_common,
        titulo='Common MAC Addresses',
        cor='purple',
        largura=13,
        altura=4
    )

    # Extraindo categorias e valores de mac_counter (Counter)
    image_counter = cria_grafico_dinamico(
        categorias=list(mac_data["mac_counter"].keys()),
        valores=list(mac_data["mac_counter"].values()),
        titulo='MAC Counter',
        cor='red',
        largura=13,
        altura=4
    )
    
    # Analise RIP #######################################################################
    rip_data = analise_rip()

    # Preparar dados para os gráficos de RIP
    image_command_response = cria_grafico_dinamico(
        categorias=['Command Response'],
        valores=[rip_data["count_command_response"]],
        titulo='Count of Command Response',
        cor='blue',
        largura=8,
        altura=4
    )

    image_routes = cria_grafico_dinamico(
        categorias=['Routes'],
        valores=[rip_data["count_routes"]],
        titulo='Count of Routes',
        cor='green',
        largura=8,
        altura=4
    )

    image_versions = cria_grafico_dinamico(
        categorias=['Version 1', 'Version 2'],
        valores=[rip_data["count_v1_version"], rip_data["count_v2_version"]],
        titulo='RIP Versions',
        cor='purple',
        largura=8,
        altura=4
    )

    # Extraindo categorias e valores de top3_next_hops (lista de tuplas)
    top3_next_hops = rip_data["top3_next_hops"]
    categorias_next_hops = [hop for hop, _ in top3_next_hops]
    valores_next_hops = [count for _, count in top3_next_hops]

    image_next_hops = cria_grafico_dinamico(
        categorias=categorias_next_hops,
        valores=valores_next_hops,
        titulo='Top 3 Next Hops',
        cor='red',
        largura=8,
        altura=4
    )


    # Análise UDP #######################################################################
    udp_data = analise_udp()

    # Preparar dados para os gráficos de UDP
    image_hop_limits = cria_grafico_dinamico(
        categorias=[str(key) for key in udp_data["hop_limits"].keys()],
        valores=list(udp_data["hop_limits"].values()),
        titulo='Hop Limits',
        cor='blue',
        largura=8,
        altura=4
    )

    image_checksums = cria_grafico_dinamico(
        categorias=list(map(str, udp_data["checksums"].keys())),
        valores=list(udp_data["checksums"].values()),
        titulo='Checksums Status',
        cor='green',
        largura=8,
        altura=4
    )

    image_source_ports = cria_grafico_dinamico(
        categorias=list(map(str, udp_data["source_ports"].keys())),
        valores=list(udp_data["source_ports"].values()),
        titulo='Source Ports',
        cor='purple',
        largura=8,
        altura=4
    )

    image_destination_ports = cria_grafico_dinamico(
        categorias=list((map(str, udp_data["destination_ports"].keys()))),
        valores=list(udp_data["destination_ports"].values()),
        titulo='Destination Ports',
        cor='red',
        largura=8,
        altura=4
    )
    # Análise TCP #######################################################################
    tcp_data = analise_tcp()

    # Gráficos de TCP usando a função cria_grafico_dinamico
    image_source_ports_tcp = cria_grafico_dinamico(
        categorias=[str(port) for port, _ in tcp_data["source_ports"]],
        valores=[count for _, count in tcp_data["source_ports"]],
        titulo='Source Ports',
        cor='blue',
        largura=8,
        altura=4
    )

    image_destination_ports_tcp = cria_grafico_dinamico(
        categorias=[str(port) for port, _ in tcp_data["destination_ports"]],
        valores=[count for _, count in tcp_data["destination_ports"]],
        titulo='Destination Ports',
        cor='green',
        largura=8,
        altura=4
    )

    image_flags = cria_grafico_dinamico(
        categorias=[flag for flag, _ in tcp_data["flags_counter"]],
        valores=[count for _, count in tcp_data["flags_counter"]],
        titulo='TCP Flags',
        cor='purple',
        largura=8,
        altura=4
    )

    image_checksums_tcp = cria_grafico_dinamico(
        categorias=list(tcp_data["checksums"].keys()),
        valores=list(tcp_data["checksums"].values()),
        titulo='Checksums Status',
        cor='red',
        largura=8,
        altura=4
    )

    # Análise TLS #######################################################################
    tls_data = analise_http()

    # Gráficos TLS usando a função cria_grafico_dinamico
    image_tls_versions = cria_grafico_dinamico(
        categorias=[version for version, _ in tls_data["tls_versions"]],
        valores=[count for _, count in tls_data["tls_versions"]],
        titulo='TLS Versions',
        cor='orange',
        largura=8,
        altura=4
    )

    image_content_types = cria_grafico_dinamico(
        categorias=[content_type for content_type, _ in tls_data["content_types"]],
        valores=[count for _, count in tls_data["content_types"]],
        titulo='Content Types',
        cor='cyan',
        largura=8,
        altura=4
    )

    # Análise DNS #######################################################################
    dns_data = analise_dns()

    # Gráficos DNS usando a função cria_grafico_dinamico
    image_query_counts = cria_grafico_dinamico(
        categorias=[str(count) for count, _ in dns_data['query_counts']],
        valores=[count for _, count in dns_data['query_counts']],
        titulo='Query Counts',
        cor='blue',
        largura=8,
        altura=4
    )

    image_answer_counts = cria_grafico_dinamico(
        categorias=[str(count) for count, _ in dns_data['answer_counts']],
        valores=[count for _, count in dns_data['answer_counts']],
        titulo='Answer Counts',
        cor='green',
        largura=8,
        altura=4
    )

    image_authority_counts = cria_grafico_dinamico(
        categorias=[str(count) for count, _ in dns_data['authority_counts']],
        valores=[count for _, count in dns_data['authority_counts']],
        titulo='Authority Counts',
        cor='purple',
        largura=8,
        altura=4
    )

    image_additional_counts = cria_grafico_dinamico(
        categorias=[str(count) for count, _ in dns_data['additional_counts']],
        valores=[count for _, count in dns_data['additional_counts']],
        titulo='Additional Counts',
        cor='orange',
        largura=8,
        altura=4
    )

    image_query_names = cria_grafico_dinamico(
        categorias=[name for name, _ in dns_data['query_names']],
        valores=[count for _, count in dns_data['query_names']],
        titulo='Query Names',
        cor='cyan',
        largura=8,
        altura=4
    )

    image_response_names = cria_grafico_dinamico(
        categorias=[name for name, _ in dns_data['response_names']],
        valores=[count for _, count in dns_data['response_names']],
        titulo='Response Names',
        cor='magenta',
        largura=8,
        altura=4
    )

    image_query_types = cria_grafico_dinamico(
        categorias=[type_ for type_, _ in dns_data['query_types']],
        valores=[count for _, count in dns_data['query_types']],
        titulo='Query Types',
        cor='red',
        largura=8,
        altura=4
    )

    image_response_types = cria_grafico_dinamico(
        categorias=[type_ for type_, _ in dns_data['response_types']],
        valores=[count for _, count in dns_data['response_types']],
        titulo='Response Types',
        cor='brown',
        largura=8,
        altura=4
    )

    image_response_codes = cria_grafico_dinamico(
        categorias=[code for code, _ in dns_data['response_codes']],
        valores=[count for _, count in dns_data['response_codes']],
        titulo='Response Codes',
        cor='grey',
        largura=8,
        altura=4
    )

    # Análise SNMP #######################################################################
    snmp_data = analise_snmp()

    # Gráficos SNMP usando a função cria_grafico_dinamico
    image_versions_snmp = cria_grafico_dinamico(
        categorias=[version for version, _ in snmp_data["count_versions"]],
        valores=[count for _, count in snmp_data["count_versions"]],
        titulo='SNMP Versions',
        cor='blue',
        largura=8,
        altura=4
    )

    image_communities = cria_grafico_dinamico(
        categorias=[community for community, _ in snmp_data["count_communities"]],
        valores=[count for _, count in snmp_data["count_communities"]],
        titulo='SNMP Communities',
        cor='green',
        largura=8,
        altura=4
    )

    image_data = cria_grafico_dinamico(
        categorias=[data for data, _ in snmp_data["count_data"]],
        valores=[count for _, count in snmp_data["count_data"]],
        titulo='SNMP Data',
        cor='purple',
        largura=8,
        altura=4
    )

    image_request_ids = cria_grafico_dinamico(
        categorias=[request_id for request_id, _ in snmp_data["count_request_ids"]],
        valores=[count for _, count in snmp_data["count_request_ids"]],
        titulo='SNMP Request IDs',
        cor='orange',
        largura=8,
        altura=4
    )

    image_error_statuses = cria_grafico_dinamico(
        categorias=[status for status, _ in snmp_data["count_error_statuses"]],
        valores=[count for _, count in snmp_data["count_error_statuses"]],
        titulo='SNMP Error Statuses',
        cor='cyan',
        largura=8,
        altura=4
    )

    image_error_indices = cria_grafico_dinamico(
        categorias=[index for index, _ in snmp_data["count_error_indices"]],
        valores=[count for _, count in snmp_data["count_error_indices"]],
        titulo='SNMP Error Indices',
        cor='magenta',
        largura=8,
        altura=4
    )

    image_variable_bindings = cria_grafico_dinamico(
        categorias=[binding for binding, _ in snmp_data["count_variable_bindings"]],
        valores=[count for _, count in snmp_data["count_variable_bindings"]],
        titulo='SNMP Variable Bindings',
        cor='red',
        largura=8,
        altura=4
    )

    image_names = cria_grafico_dinamico(
        categorias=[name for name, _ in snmp_data["count_names"]],
        valores=[count for _, count in snmp_data["count_names"]],
        titulo='SNMP Object Names',
        cor='brown',
        largura=12,
        altura=4
    )
    image_responses_to = cria_grafico_dinamico(
        categorias=[response_to for response_to, _ in snmp_data["count_responses_to"]],
        valores=[count for _, count in snmp_data["count_responses_to"]],
        titulo='SNMP Responses To',
        cor='blue',
        largura=8,
        altura=4
    )
    # Incluir os gráficos no contexto
    context = {
        'grafico_base64': image_base64,
        'trabalho_1_ips': image_trabalho_1_ips,
        'trabalho_2_arp_unicos': image_unique,
        'trabalho_2_arp_reply': image_reply,
        'trabalho_2_arp_comuns': image_common,
        'trabalho_2_arp_counter': image_counter,
        'trabalho_3_rip_response':image_command_response,
        'trabalho_3_rip_routes':image_routes,
        'trabalho_3_rip_versions':image_versions,
        'trabalho_3_rip_next_hops_comuns':image_next_hops,
        'trabalho_4_udp_hop_limits':image_hop_limits,
        'trabalho_4_udp_checksums_status':image_checksums,
        'trabalho_4_udp_source_ports':image_source_ports,
        'trabalho_4_udp_destination_ports':image_destination_ports,
        'trabalho_5_tcp_source_ports':image_source_ports_tcp,
        'trabalho_5_tcp_image_destionation_ports':image_destination_ports_tcp,
        'trabalho_5_tcp_image_flags':image_flags,
        'trabalho_5_tcp_checksums':image_checksums_tcp,
        'trabalho_6_tls_versions':image_tls_versions,
        'trabalho_6_tls_content_typers':image_content_types,
        'trabalho_7_dns_query':image_query_counts,
        'trabalho_7_dns_answer_counts':image_answer_counts,
        'trabalho_7_dns_autority_counts':image_authority_counts,
        'trabalho_7_dns_additional':image_additional_counts,
        'trabalho_7_dns_query_names':image_query_names,
        'trabalho_7_dns_response_names':image_response_names,
        'trabalho_7_dns_query_types':image_query_types,
        'trabalho_7_dns_response_types':image_response_types,
        'trabalho_7_dns_response_codes':image_response_codes,
        'trabalho_8_snmp_versions':image_versions_snmp,
        'trabalho_8_snmp_comunities':image_communities,
        'trabalho_8_snmp_data':image_data,
        'trabalho_8_snmp_request_ids':image_request_ids,
        'trabalho_8_snmp_erro_status':image_error_statuses,
        'trabalho_8_snmp_error_index':image_error_indices,
        'trabalho_8_snmp_variable_bindings':image_variable_bindings,
        'trabalho_8_snmp_names':image_names,
        'trabalho_8_snmp_responses_to':image_responses_to,
    }

    return render(request, 'charts.html', context)
