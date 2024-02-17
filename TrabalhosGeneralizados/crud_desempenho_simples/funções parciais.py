from functools import partial

def funcao_parcial(prefixo, sufixo=0):
    mensagem = f"{prefixo} Eu sou burro {sufixo}"
    print(mensagem)

# Criando uma função parcial com o argumento "prefixo" fixo
funcao_parcial_fixa = partial(funcao_parcial, "Olá,")

# Chamando a função parcial
funcao_parcial_fixa(sufixo="!")

funcao_parcial_fixa()

# Output esperado: Olá, Eu sou burro !
