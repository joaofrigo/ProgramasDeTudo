import mysql.connector

connection = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
) # uma função que usaa um dicionário como argumento

cursor = connection.cursor()

print("Teste dos nomes das colunas(antes da execução da query de select): " + str(cursor.column_names))
codigoSQL = "SELECT * from json"
#print("Teste dos nomes das colunas: " + str(cursor.column_names))

cursor.execute(codigoSQL)
resultado = cursor.fetchall() # o fetchall pega todos os valores resultados da query, todo o output da query.
print("Teste dos nomes das colunas(depois da execução da query de select): " + str(cursor.column_names)) # Não existia
# Antes porque o cursos não sabia a qual tabela estavamos nos referindo.
print("O resultado do select * com o fetchall() " + str(resultado)) # o select * pega todos os valores da tabela, e
# o fetch all todo o output da query(que no caso a query foi de pegar todos os valores da tebela)

cursor.close()
connection.close()

print()
print("Dando print de cada valor da tupla de colunas individualmente:")
for resultado in resultado:
    print(resultado) # mesma maneira de fazer o print da tupla resultado. só não troca ela por string nesse caso.
    # Nesse caso ela pega a string dentro da tupla, no outro, transforma em string a tupla de vetores de string.