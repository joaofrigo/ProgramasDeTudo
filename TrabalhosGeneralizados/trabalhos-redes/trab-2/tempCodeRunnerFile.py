    mac_addresses = set()  # Usar um set para evitar endereços MAC duplicados
    reply_mac_addresses = set()  # Usar um set para endereços MAC que responderam a ARP
    mac_counter = Counter()  # Contador para a frequência dos endereços MAC
    
    for pacote in pacotes:
        try:
            # Extraindo endereços MAC da camada ARP
            src_mac_arp = pacote.arp.src_hw_mac
            dst_mac_arp = pacote.arp.dst_hw_mac
            mac_addresses.add(src_mac_arp)
            mac_addresses.add(dst_mac_arp)
            mac_counter.update([src_mac_arp, dst_mac_arp])

            # Extraindo endereços MAC da camada Ethernet
            src_mac_eth = pacote.eth.src
            dst_mac_eth = pacote.eth.dst
            mac_addresses.add(src_mac_eth)
            mac_addresses.add(dst_mac_eth)
            mac_counter.update([src_mac_eth, dst_mac_eth])

            # Verificar se o pacote é uma resposta ARP (opcode == 2)
            if pacote.arp.opcode == '2':
                reply_mac_addresses.add(src_mac_arp)
        except AttributeError:
            continue

    # Converter conjuntos para listas para facilitar o retorno
    mac_addresses_list = list(mac_addresses)
    reply_mac_addresses_list = list(reply_mac_addresses)
    
    # Obter os endereços MAC mais comuns
    common_mac_addresses = mac_counter.most_common()

    return {
        "unique_mac_addresses": mac_addresses_list,
        "reply_mac_addresses": reply_mac_addresses_list,
        "common_mac_addresses": common_mac_addresses,
        "mac_counter": mac_counter
    }