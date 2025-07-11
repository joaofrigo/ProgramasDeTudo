import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('D888199_2021-2022.csv', encoding='utf-8')

# 2. Removendo a coluna '%' do DataFrame, os valores estão inconsistentes, logo irrelevantes
data = data.drop(columns=['%'])

total_alunos = data['Alunos'].sum()
print(f"Total de Alunos no CSV: {total_alunos}")

# Como raios a tabela de valores funciona?