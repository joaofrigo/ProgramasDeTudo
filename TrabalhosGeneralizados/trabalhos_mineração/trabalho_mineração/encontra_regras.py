import json
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import numpy
numpy.random.seed(12345) # mantendo a mesma seed para reprodutibilidade de regras

# ajustando o limite de linhas do display do print
pd.set_option('display.max_rows', 25)  
pd.set_option('display.min_rows', 25)   

with open('padaria_caracteres_corretos.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# extrair as transações (listas de produtos) do JSON
transacoes = [compra["produtos"] for compra in data]

# preparamos os dados para a mineração
te = TransactionEncoder() # pegamos o objeto para a codificação correta pro apriori (0 1)
# print(te.fit(transacoes))
# print(te.fit(transacoes).transform(transacoes))
"""
exemplo de como a transformação fica para o apriori
[[1, 1, 1, 0]: Queijo, Pão, Presunto
 [1, 0, 1, 1]: Queijo, Presunto, Refri
 [1, 1, 0, 0]: Queijo, Pão
 [0, 0, 1, 1]]: Presunto, Refri
"""
transacoes_encoded = te.fit_transform(transacoes) 
df_transacoes = pd.DataFrame(transacoes_encoded, columns=te.columns_) # criamos o dataframe

# usamos apriori e geramos regras
frequent_items = apriori(df_transacoes, min_support=0.02, use_colnames=True) # apriori aceita dataframes ou matriz binária
regras = association_rules(frequent_items, metric="confidence", min_threshold=0.25) # ajustamos os minimos de acordo, lembrando:
# suporte é quantidade de vezes que o item aparece. threshold é a qualidade da regra 

# pego as listas de só um valor. no caso, as relações de 1 a 1 antecedente e consequente
regras_1a1 = regras[regras['antecedents'].str.len().eq(1) & regras['consequents'].str.len().eq(1)]

# ordenar e selecionar as regras 1 para 1
top_regras_1a1 = regras_1a1.sort_values(by="confidence").head(5)

# mostrar 5 regras 1 para 1
print("5 regras 1 para 1:")
print(top_regras_1a1[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# encontramos o mais influente de 1 para 1
regras_1a1_fortes = regras_1a1[regras_1a1['confidence'] > 0.3]
produtos_mais_influentes = regras_1a1_fortes['antecedents'].apply(lambda x: list(x)[0]).value_counts()
produto_mais_influente = produtos_mais_influentes.idxmax()
print(f"\nProduto mais influente: {produto_mais_influente}")
# o produto mais forte tem confidence e lift altos, além de vários antecedents.

# filtramos regras de doce
regras_doce = regras[regras['antecedents'].apply(lambda x: any('Doce' in item for item in x)) | 
                     regras['consequents'].apply(lambda x: any('Doce' in item for item in x))]
# a filtragem ocorre aplicando uma função que retornara true ou false para o any(). Se existe string 'Doce', em qualquer
# lugar dos items na regra de antecedentes OU consequentes, retorna um true e adiciona isso para uma regra de doce

print("\nRegras que implicam a compra de 'Doce':")
print(regras_doce[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# todas as regras
print("\nTodas as regras:")
print(regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']])





"""
Fatos interessantes: 
as regras de 1 para 1 de café com pão francês, todas tem o mesmo suporte
(Pão Francês)    (Café Melita)  0.02439    0.107143  0.775210
(Pão Francês)    (Café Nestle)  0.02439    0.107143  1.317857

"""