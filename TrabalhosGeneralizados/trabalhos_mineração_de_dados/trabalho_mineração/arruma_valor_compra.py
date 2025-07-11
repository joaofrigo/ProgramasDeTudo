import json

with open('padaria.json', 'r') as file:
    dados = json.load(file)

# modificar o ID de compra
for i, compra in enumerate(dados):
    compra['compra'] = i + 1  

with open('padaria_compra_correta.json', 'w') as file:
    json.dump(dados, file, indent=4)

"""
Os erros encontrados de sintaxe do json
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 738 column 4 (char 14595)

"""