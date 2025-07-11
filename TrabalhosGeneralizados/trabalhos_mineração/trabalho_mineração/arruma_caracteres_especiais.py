import json

# devemos abrir usando encoding correto para ler os caracteres especiais
with open('padaria_compra_correta.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# prova que os caracteres estão corretos
for compra in dados:
    print(compra)

# precisamos usar o mesmo encoding no open para ler os caracteres, depois ensure_ascii no false.
# se não fizermos assim, ou os caracteres continuam especiais como default, ou não lemos eles corretamente
with open('padaria_caracteres_corretos.json', 'w', encoding='utf-8') as file:
    json.dump(dados, file, ensure_ascii=False, indent=4)
