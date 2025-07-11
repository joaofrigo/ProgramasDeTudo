import pandas as pd
import glob

# Lista com os nomes dos arquivos CSV a serem combinados
arquivos = [
    'D200888_2021.csv',
    'D200888_2023.csv',
    'D320200_2021-2022.csv',
    'D402855_2021.csv',
    'D402855_2022.csv',
    'D402855_2023.csv',
    'D888148_2021.csv',
    'D888148_2022.csv',
    'D888148_2022.csv',
    'D888200_2021-2022.csv'
]

# Lista para armazenar os DataFrames
dfs = []

# Ler cada arquivo CSV e adicioná-lo à lista
for arquivo in arquivos:
    df = pd.read_csv(arquivo)
    dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df_unificado = pd.concat(dfs, ignore_index=True)

# Salvar o DataFrame unificado em um novo arquivo CSV
df_unificado.to_csv('df_unificado.csv', index=False)

print("Os arquivos foram combinados com sucesso!")
