# Componente primordial
class Cafe:
    def custo(self) -> float:
        return 5.0

# Decorator que adiciona funcionalidades pro componente primordial
class DecoradorCafe:
    def __init__(self, cafe: Cafe):
        self.cafe = cafe

    def custo(self) -> float:
        pass

# Decorator funcionalidade
class Leite(DecoradorCafe):
    def custo(self) -> float:
        return self.cafe.custo() + 2.0

# Decorator funcionalidade
class Acucar(DecoradorCafe):
    def custo(self) -> float:
        return self.cafe.custo() + 1.0

# Decorator funcionalidade
class Canela(DecoradorCafe):
    def custo(self) -> float:
        return self.cafe.custo() + 1.5
    
# Exemplo de Uso
cafe_simples = Cafe()

# Decorando o café com leite
cafe_com_leite = Leite(cafe_simples)
print(f"Café com Leite: {cafe_com_leite.custo()}")

# Decorando o café com açúcar e canela
cafe_especial = Canela(Acucar(cafe_simples))
print(f"Café Especial: {cafe_especial.custo()}")

