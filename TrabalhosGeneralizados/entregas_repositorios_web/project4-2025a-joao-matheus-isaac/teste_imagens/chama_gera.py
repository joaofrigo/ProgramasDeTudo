from gera import gerar_imagem_flux

def chamar_gera(descricao):
    return gerar_imagem_flux(descricao)

saida = chamar_gera("guerreiro ciborgue com armadura azul e fundo futurista")
print(f"Imagem salva em: {saida}")
