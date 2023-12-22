import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="FATEC",
  password="serverEaD",
  database="jsonparsed"
) # uma função que usaa um dicionário como argumento

cursor = connection.cursor()

codigoSQL = "INSERT INTO json (Json, URL) VALUES (%s,%s);" # coloca na tabela json, nos valores Json e Url, string string

informacao = (
  'colocou um json',
  'colocou uma url',
)

cursor.execute(codigoSQL, informacao) # Executa o código SQL com as informações do %s e do %s preenchidas.
connection.commit() # Manda para a base de dados salvar.

print("A operação funfou")

IDJson = cursor.lastrowid

cursor.close
connection.close

print("O ID do Json inserido agora é: ", IDJson)
# Fecha a conexão e o que manda coisas para a conexão. Cursor é basicamente o file, e o connection é o fileopen
