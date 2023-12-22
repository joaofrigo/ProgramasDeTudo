import os

nome_arquivo = 'ArquivoJsonTeste'

#Caminho completo para o arquivo
caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
# o método path.dirname retorna o diretório onde está sendo executando o arquivo python