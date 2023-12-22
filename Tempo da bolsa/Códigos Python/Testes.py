print("hello world em python")
age = 20
print(age)
age="nada"
print(age)
age=False
print(age)
age={1,2,3}
print(age)
age = input("Seu boco chamado de ")
print("Ola seu boco string " + age)
#int(age)
#print("Ola seu boco int " + age)
#float(age)
#print("Ola seu boco float " + age)
age = int(age) + int(age)
print("Ola seu boco somado a si mesmo de maneira string " + str(age))
#precisou do string, por que não se concatena int com string no print nem em qualquer outor lugar basicamente.
testeFloat = float(input("oto criativo "))
print ("aqui está o bobo float noveo " + str(testeFloat))
#testeFloat.upper # significa dizer que ele reconhece que antes de ser convertido, ele não é string.
testeFloat = str(testeFloat)
testeFloat.upper # só agora a função reconhece.
testeFind = "String gigantrolha"
print("teste do find " + str(testeFind.find('t'))) # ele avisa aonde ele encontrou primeiro no vetor o caracter ou sequencia de caracteres.
#ovo usa isso no parser
#tem outra maneira de usar o find e ser fácil com a vida usando .replace
print("teste do replace " + str(testeFind.replace('String', 'batata')))
# se eles não acham nada dá -1
print("Existe isso na string?\n" + str("String" in testeFind))
if testeFind == "batata": # Pode se colocar os parenteses, mas está só mudando a ordenação aritmética da coisa
    print ("oi")
# a indentação define o bloco de código.
elif testeFind.find("ba"):
    print("tchau")
else:
    print("como")
for x in range(5):
    print(x * 'Piramide-')

lista = [1,2,3,"batata",True]
print(str(lista[0]))
print(lista[3])
print("Agora todos: " + str(lista[0:5])) #Ele nem avisa se o vetor explode pegando todas as listas. Ele só ignora
#Ele começa contando de 0 e vai até o vetor posição 4, meio bobinho e invertido.
for x in lista:
    x = 3
    #Valor não se altera sozinho.
lista.insert(0, False) #lembrar de ver as propiedadas da função passando mouse em cima, isso aceita um int index e um objeto qualquer
for x in lista:
    print("Agora um por vez " + str(x))

#Agora que inserimos na lista, tem mais um valor na lista como óbivo
lista.remove(1)
print(lista[0:len(lista)]) # O len retorna o tamanho da lista. O remove claramente remove
print(lista[0:lista.__sizeof__()]) # O sizeof retorna o mesmo que a lista com len.
lista.clear()
print(lista[0:lista.__sizeof__()]) # agora o clear limpa tudo de fato.
print("Agora quem usa de maneira normal e humana pra printar os valores da lista: " + str(lista))

for valor in range(0,5):
    lista.insert(valor, valor)

print("Colocou os valores de novo na lista com range")

for valor in lista:
    print(str(valor))

# o símbolo ++ não existe, por que não existem operadores em python, apenas statements.

valor = (1,2,3) # criação de tupla, as constantes do python
valor = (5) # ainda uma tupla no final das contas

print(dir(valor))
#print(help(valor))

#criando um dicionário:

estudante = {"Nome": "luigi", "País": "Reino dos cogumelos", "Habilidades": ["Smash turts", "Be cringe"], 3: [1,2,3,"Yes"]}
print(estudante)
print("Ovo usa o índice funny do dicionário " + estudante["Nome"])
print("Ovo usa o índice funny do dicionário " + estudante["País"])
print("Ovo usa o índice funny do dicionário " + str(estudante["Habilidades"])) #lista de strings
print("Ovo usa o índice funny do dicionário " + str(estudante[3])) #lista de ints com string
print("Ovo usa o índice funny do dicionário " + str(estudante.get("Irmão"))) # O get impede que o programa morra por falta de key
print("Ovo usa o índice funny do dicionário " + str(estudante.get("Irmão", "Não tem")))
estudante ["Irmão"] = "Mario"
print("Ovo usa o índice funny do dicionário " + str(estudante.get("Irmão", "Não tem")))
estudante.update({"Nome": "mario", "Irmão": "luigi", "ComidaPreferida": "Espaguete"})
print(estudante)
mario = estudante.pop("Nome")
print(mario)
print(estudante.get("Nome"))
print(estudante.keys(), "\n", len(estudante), "\n" , estudante.values(), "\n", estudante.items())
for keys, items in estudante.items():
    print(keys, ":" , items)
del estudante

# então ao invés de um erro keyword, recebemos apenas um "none", funcionalmente similar ao try catch. Só lembrar que é função.

