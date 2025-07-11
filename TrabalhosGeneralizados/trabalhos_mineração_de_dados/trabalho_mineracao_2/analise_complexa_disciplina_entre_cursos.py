import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

data = pd.read_csv('D888199_2021-2022.csv')

data['Reprovado'] = (data['Situação'] == 'Reprovado').astype(int)

data = data.dropna(subset=['Cód. Turma', 'Professor', 'Alunos', 'Reprovado'])

if data.empty:
    raise ValueError("Os dados estão vazios após a remoção de valores ausentes.")

data['Cód. Turma'] = data['Cód. Turma'].astype(str)
data['Professor'] = data['Professor'].astype(str)

data = pd.get_dummies(data, columns=['Cód. Turma', 'Professor'], drop_first=True)

X = data.drop(columns=['Situação', 'Reprovado'])
y = data['Reprovado']

X = X.apply(pd.to_numeric, errors='coerce')
X = X.dropna()

if X.empty or y.empty:
    raise ValueError("Os dados de entrada (X ou y) estão vazios após a remoção de valores ausentes.")

X = sm.add_constant(X)

X_vif = X.drop('const', axis=1)
vif_data = pd.DataFrame()
vif_data['Variable'] = X_vif.columns
vif_data['VIF'] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]

print("\nVIF DataFrame:")
print(vif_data)

model = sm.Logit(y, X)
result = model.fit()

print("\nResumo do modelo de regressão logística:")
print(result.summary())
