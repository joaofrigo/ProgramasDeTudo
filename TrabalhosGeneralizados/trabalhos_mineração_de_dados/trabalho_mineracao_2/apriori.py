import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carregar o CSV
df = pd.read_csv('D888199_2021-2022.csv')

# Criar uma tabela de presença/ausência para os cursos (1 para "Aprovado", 0 para outros casos)
basket = df.pivot_table(index='Alunos', columns='Curso', values='Situação', 
                        aggfunc=lambda x: 1 if 'Aprovado' in x.values else 0, fill_value=0)

# Converter os valores para booleanos
basket = basket.astype(bool)

# Verificar o conteúdo do DataFrame 'basket'
print("Tabela de presença/ausência:")
print(basket.head())

# Encontrar itemsets frequentes com suporte mínimo de 0.05 (ajustar conforme necessário)
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)

# Verificar se há itemsets frequentes antes de continuar
if frequent_itemsets.empty:
    print("Nenhum itemset frequente encontrado.")
else:
    print("Itemsets frequentes encontrados:")
    print(frequent_itemsets)

    # Gerar regras de associação com confiança mínima de 0.7 (ajustar conforme necessário)
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.7)

    # Verificar se há regras geradas
    if rules.empty:
        print("Nenhuma regra de associação encontrada.")
    else:
        # Selecionar colunas relevantes e exibir de forma compacta
        regras_compactas = rules[['antecedents', 'consequents', 'support', 'confidence']]

        # Exibir as regras de forma formatada
        # Exibindo as regras de forma mais legível
        for index, row in regras_compactas.iterrows():
            antecedentes = ', '.join(list(row['antecedents']))
            consequentes = ', '.join(list(row['consequents']))
            print(f"Regra {index + 1}:")
            print(f"Antecedentes: {antecedentes}")
            print(f"Consequentes: {consequentes}")
            print(f"Suporte: {row['support']:.2f}")
            print(f"Confiança: {row['confidence']:.2f}")
            print("-" * 50)
