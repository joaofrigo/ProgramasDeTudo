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