import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Formato do csv: Ano,Semestre,Cód. Disciplina,Cód. Turma,Situação,%,Alunos,Professor,Cód. Curso,Curso

# Configuração de visualização
sns.set(style="whitegrid")

# 1. Carregando o arquivo CSV
data = pd.read_csv('D888199_2021-2022.csv', encoding='utf-8')

# 2. Removendo a coluna '%' do DataFrame, os valores estão inconsistentes, logo irrelevantes
data = data.drop(columns=['%'])


# 7. Analisando a distribuição de aprovação e reprovação
status_counts = data['Situação'].value_counts()
print("Distribuição de Situação dos Alunos:")
print(status_counts)

# Visualizando a distribuição de status com um gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis')
plt.title('Distribuição de Situação dos Alunos')
plt.xlabel('Situação')
plt.ylabel('Número de Alunos')
plt.show()

# 14. Calculando a taxa de aprovação ponderada por professor (considerando o total de alunos)
approval_rate_by_professor = data[data['Situação'] == 'Aprovado'].groupby('Professor').apply(
    lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()
).sort_values(ascending=False)

print("Taxa de Aprovação Ponderada por Professor:")
print(approval_rate_by_professor)

# Visualizando a taxa de aprovação média ponderada por professor
plt.figure(figsize=(14, 7))
approval_rate_by_professor.plot(kind='bar', color='steelblue')
plt.title('Taxa Média de Aprovação Ponderada por Professor')
plt.xlabel('Professor')
plt.ylabel('Porcentagem Média de Aprovação')
plt.xticks(rotation=45)
plt.tight_layout()  # Ajusta o layout para que os rótulos não fiquem cortados
plt.show()

#######
# 1. Filtrando apenas as reprovações
reprovacao_data = data[data['Situação'] == 'Reprovado']

# 2. Calculando a média ponderada de reprovação por professor e turma
reprovacao_rate_by_professor_turma = reprovacao_data.groupby(['Professor', 'Cód. Turma']).apply(
    lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()
).sort_values(ascending=False)

print("Taxa de Reprovação Ponderada por Professor e Turma:")
print(reprovacao_rate_by_professor_turma)

# 3. Extraindo o Top 10 de professores e turmas com maior taxa de reprovação
top_10_reprovacao = reprovacao_rate_by_professor_turma.head(10)

print("Top 10 Professores e Turmas com maior taxa de reprovação:")
print(top_10_reprovacao)

# 4. Visualizando os dados em um gráfico de barras
plt.figure(figsize=(14, 7))
top_10_reprovacao.plot(kind='bar', color='tomato')
plt.title('Top 10 Professores e Turmas com Maior Taxa de Reprovação')
plt.xlabel('Professor e Turma')
plt.ylabel('Porcentagem Média de Reprovação')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Ajusta o layout para melhor visualização
plt.show()

# 9. Analisando a taxa de aprovação por curso
# Calculando a taxa de aprovação ponderada por número de alunos
approval_rate_by_course = data[data['Situação'] == 'Aprovado'].groupby('Curso').apply(
    lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()
).sort_values(ascending=False)

print("Taxa de Aprovação Ponderada por Curso:")
print(approval_rate_by_course)

# Visualizando a taxa de aprovação média por curso
plt.figure(figsize=(14, 7))
approval_rate_by_course.plot(kind='bar', color='lightcoral')
plt.title('Taxa Média de Aprovação por Curso')
plt.xlabel('Curso')
plt.ylabel('Porcentagem Média de Aprovação')

# Ajustando a rotação e tamanho da fonte dos rótulos
plt.xticks(rotation=45, ha='right', fontsize=10)

# Exibindo a plotagem
plt.tight_layout()  # Ajusta o layout para que os rótulos não fiquem cortados
plt.show()

# 10. Analisando a correlação entre a porcentagem de alunos e a taxa de aprovação
data['Alunos'] = pd.to_numeric(data['Alunos'], errors='coerce')
correlation = data[['%', 'Alunos']].corr()
print("Correlação entre % e Número de Alunos:")
print(correlation)

# 13. Verificando a média de aprovação ponderada por turma (considerando o total de alunos)
approval_rate_by_turma = data[data['Situação'] == 'Aprovado'].groupby('Cód. Turma').apply(
    lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()
).sort_values(ascending=False)

print("Média de Aprovação Ponderada por Turma:")
print(approval_rate_by_turma)

# Plotando a média de aprovação ponderada por turma
plt.figure(figsize=(14, 7))
approval_rate_by_turma.plot(kind='bar', color='lightgreen')
plt.title('Média de Aprovação Ponderada por Turma')
plt.xlabel('Código da Turma')
plt.ylabel('Porcentagem Média de Aprovação')
plt.xticks(rotation=45)
plt.tight_layout()  # Ajusta o layout para que os rótulos não fiquem cortados
plt.show()


# Filtrando os dados para o professor específico
turmas_professor = data[data['Professor'] == 'A292200218320']

# Calculando a taxa de aprovação ponderada por turma para o professor
taxas_turma = turmas_professor.groupby('Cód. Turma')[['%', 'Alunos']].apply(
    lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()
).sort_values(ascending=False)

# Exibindo as taxas de aprovação por turma
print(taxas_turma)

# Visualizando as taxas de aprovação por turma com um gráfico de barras
plt.figure(figsize=(14, 7))
taxas_turma.plot(kind='bar', color='skyblue')
plt.title('Taxa de Aprovação por Turma para o Professor A292200218320')
plt.xlabel('Código da Turma')
plt.ylabel('Porcentagem Média de Aprovação')
plt.xticks(rotation=45)
plt.tight_layout()  # Ajusta o layout para que os rótulos não fiquem cortados
plt.show()






# 14. Exibindo os resultados finais
print("Análise concluída!")
