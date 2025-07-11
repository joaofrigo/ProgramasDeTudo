import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Carregar o CSV unificado
df = pd.read_csv('df_unificado.csv')

# Criar uma variável binária para indicar aprovação (1) ou reprovação (0)
df['Aprovado'] = df['Situação'].apply(lambda x: 1 if x == 'Aprovado' else 0)

# Calcular a média de aprovação por curso
curso_stats = df.groupby('Curso')['Aprovado'].mean().reset_index()
curso_stats.rename(columns={'Aprovado': 'Media_Taxa_Aprovacao_Curso'}, inplace=True)

# Adicionar média de aprovação por curso ao dataframe principal
df = pd.merge(df, curso_stats, on='Curso', how='left')

# Calcular o desempenho relativo do professor
df['Desempenho_Relativo'] = df['Aprovado'] - df['Media_Taxa_Aprovacao_Curso']

# Agrupar por professor para criar variáveis agregadas
professor_stats = df.groupby('Professor').agg(
    Total_Aprovados=('Aprovado', 'sum'),
    Total_Reprovados=('Aprovado', lambda x: len(x) - sum(x)),
    Total_Alunos=('Alunos', 'sum'),
    Media_Taxa_Aprovacao_Curso=('Media_Taxa_Aprovacao_Curso', 'mean')
).reset_index()

# Variáveis explicativas (features) e variável alvo (target)
X = professor_stats[['Total_Aprovados', 'Total_Reprovados', 'Total_Alunos', 'Media_Taxa_Aprovacao_Curso']]
y = professor_stats['Total_Aprovados'] / professor_stats['Total_Alunos']  # Taxa de aprovação por professor

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criar e treinar o modelo de Random Forest
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Prever nos dados de teste
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Calcular métricas de desempenho
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

# Realizar validação cruzada
cross_val_scores = cross_val_score(model, X, y, cv=5, scoring='r2')

# Exibir os resultados
print("Desempenho do Modelo:")
print(f"MSE no conjunto de treinamento: {mse_train:.4f}")
print(f"MSE no conjunto de teste: {mse_test:.4f}")
print(f"R^2 Score no conjunto de treinamento: {r2_train:.4f}")
print(f"R^2 Score no conjunto de teste: {r2_test:.4f}")
print("\nR^2 Scores de validação cruzada:", cross_val_scores)
print(f"Média do R^2 Score de validação cruzada: {np.mean(cross_val_scores):.4f}")

# Importância das variáveis
importances = model.feature_importances_
coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nImportância das Variáveis:")
print(coef_df)
