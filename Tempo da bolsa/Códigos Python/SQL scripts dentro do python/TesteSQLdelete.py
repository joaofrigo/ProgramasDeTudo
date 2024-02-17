import mysql.connector

connection = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
) # uma função que usaa um dicionário como argumento

cursor = connection.cursor()

valor = input("Esse delete pode deletar todos os regristros. depende da igualdade != ou =")
codigoSQL = "DELETE FROM json WHERE id != %s" # "DELETE FROM json WHERE IDJson = %s"
# DBCC CHECKIDENT ('table_name', RESEED, new_value); serve para resetar a seed incremental da tabela.
data = (valor,) # precisa sempre ser uma tupla ou lista como argumento. Por isso a vírgula, transforma em lista.

#print(1)
cursor.execute(codigoSQL, data)
colunasAfetadas = cursor.rowcount # Vê a quantidade de colunas que foram afetadas.
codigoSQL = "ALTER TABLE json AUTO_INCREMENT = 1"
cursor.execute(codigoSQL)
#print(2)
connection.commit()
#print(3)

cursor.close()
connection.close()

print("A quantidade de colunas afetadas foi " + str(colunasAfetadas))
print("Tudo foi deletado (ou será que foi?)")