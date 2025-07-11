import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def processar_centro(file_path, centro_nome):
    df = pd.read_csv(file_path, sep=",", encoding="utf-8")
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    df = df[df["ANO"] != "TOTAL"]
    df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")
    
    # Filtra apenas ingressantes positivos e agrupa por sexo
    df_resultado = df[df["INGRESSANTES"] > 0].groupby(["ANO", "SEXO"])['INGRESSANTES'].sum().reset_index()
    df_resultado["CENTRO"] = centro_nome  # Adiciona o nome do centro aos dados processados
    
    return df_resultado

# Lista de arquivos CSV e nomes dos centros
arquivos_centros = [
    ("CT Ingressantes e formados por sexo.csv", "Centro de Tecnologia"),
    ("CCSH Ingressantes e formados por sexo.csv", "Centro de Ciências Sociais e Humanas")
]

# Processa os arquivos dos centros e combina os dados
dados_centros = pd.concat([processar_centro(caminho, nome) for caminho, nome in arquivos_centros])

# Configuração do gráfico
plt.figure(figsize=(18, 8))
anos = sorted(dados_centros["ANO"].dropna().unique())
bar_width = 0.15 
index = np.arange(len(anos))

# Gráfico para masculino e feminino separados por centro
centros = dados_centros["CENTRO"].unique()

cores = {
    "Centro de Tecnologia": {'M': '#1F77B4', 'F': '#FF7F0E'},  # Azul e laranja
    "Centro de Ciências Sociais e Humanas": {'M': '#2CA02C', 'F': '#D62728'}  # Verde e vermelho
}

# Posicionamento das barras
offsets = np.linspace(-bar_width * 1.5, bar_width * 1.5, len(centros))

# Adiciona as barras para cada centro e sexo
for i, sexo in enumerate(["M", "F"]):
    for j, centro in enumerate(centros):
        subset = dados_centros[(dados_centros["SEXO"] == sexo) & (dados_centros["CENTRO"] == centro)]
        barras = [subset[subset["ANO"] == ano]["INGRESSANTES"].values[0] if not subset[subset["ANO"] == ano].empty else 0 for ano in anos]
        color = cores[centro][sexo]  # Cor específica para o centro e sexo
        label = f"{centro} - {'Masculino' if sexo == 'M' else 'Feminino'}"

        plt.bar(index + offsets[j] + i * bar_width, barras, bar_width,
                label=label if j == 0 and i == 0 else "",  # Adiciona a legenda apenas na primeira barra de cada centro e sexo
                color=color, alpha=0.8)

# Adiciona linhas divisórias entre os anos
for i in range(1, len(anos)):
    plt.axvline(x=i - 0.5, color='black', linewidth=1, linestyle='--')

# Adiciona a legenda manualmente para cada grupo de barras
handles = []
for centro in centros:
    for sexo in ["M", "F"]:
        color = cores[centro][sexo]
        label = f"{centro} - {'Masculino' if sexo == 'M' else 'Feminino'}"
        handle = plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.8)
        handles.append(handle)
        plt.text(1.02, 1 - len(handles) * 0.025, label, transform=plt.gca().transAxes, fontsize=10, color=color)

plt.xlabel('Ano')
plt.ylabel('Número de Ingressantes')
plt.title('Número de Ingressantes por Ano e Sexo nos Centros de Ensino')
plt.xticks(index, anos, rotation=45)
plt.tight_layout()
plt.show()
