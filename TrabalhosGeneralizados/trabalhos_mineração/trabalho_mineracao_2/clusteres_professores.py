import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Leitura do CSV
data = pd.read_csv('D888199_2021-2022.csv')

# Filtrando os dados de aprovação e reprovação
aprovados = data[data['Situação'] == 'Aprovado']
reprovados = data[data['Situação'] == 'Reprovado']

# Calculando a média ponderada de aprovação e reprovação por professor
approval_summary = aprovados.groupby('Professor').apply(lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()).rename('aprovacao_media')
rejection_summary = reprovados.groupby('Professor').apply(lambda x: (x['%'] * x['Alunos']).sum() / x['Alunos'].sum()).rename('reprovacao_media')

# Combinar as médias de aprovação e reprovação em um único DataFrame
final_summary = pd.merge(approval_summary, rejection_summary, on="Professor", how="outer")
final_summary = final_summary.fillna(0)

# Normalizar os dados para clustering
scaler = StandardScaler()
summary_scaled = scaler.fit_transform(final_summary[["aprovacao_media", "reprovacao_media"]])

# Aplicar K-Means para identificar padrões
kmeans = KMeans(n_clusters=3, random_state=42)
final_summary["Cluster"] = kmeans.fit_predict(summary_scaled)

# Visualizar resultados dos clusters com escala de 0 a 100
plt.figure(figsize=(10, 6))
for cluster in final_summary["Cluster"].unique():
    cluster_data = final_summary[final_summary["Cluster"] == cluster]
    plt.scatter(
        cluster_data["aprovacao_media"],
        cluster_data["reprovacao_media"],
        label=f"Cluster {cluster}",
        s=100
    )

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title("Clusters de Professores com Base nas Taxas de Aprovação e Reprovação")
plt.xlabel("Taxa Média de Aprovação (%)")
plt.ylabel("Taxa Média de Reprovação (%)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Exibir resumo com os clusters corrigidos
print("Resumo das taxas por professor com clusters (corrigido):")
print(final_summary)