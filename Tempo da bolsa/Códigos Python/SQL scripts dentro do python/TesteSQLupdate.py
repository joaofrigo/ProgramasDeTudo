import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="FATEC",
  password="serverEaD",
  database="jsonparsed"
) # uma função que usaa um dicionário como argumento

cursor = connection.cursor()

codigoSQL = "UPDATE json SET Json = %s, URL = %s WHERE IDJson = %s" # Faça um update nas variáveis Json e URL aonde
# a chave primária (IDJson) tem esse valor.
informacao = (
    "Json updatado",
    "URL updatada",
    2 # O ID
)

cursor.execute(codigoSQL, informacao)
connection.commit()

colunasAfetadas = cursor.rowcount # Vê a quantidade de colunas que foram afetadas.

cursor.close()
connection.close()

print("A quantidade de colunas afetadas foi " + colunasAfetadas)