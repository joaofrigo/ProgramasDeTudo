// Programa 1 - (3) Renomear Método. Método estava mal descrito.
class Dados {
    private String nome = "Fujiro";
    private String sobrenome= "Nakomb";
    String getSobrenome(){
        return sobrenome;
    }
}

// Programa 2 - (2) Consolidar Fragmentos Condicionais Duplicados. O send ocorrerá sempre de qualquer maneira, evita duplicidade.
if(isOfertaEspecial(){
    total = preco * 0.95;
    }else{
    total = preco * 0.99;
}
send();

//Programa 3 - (1) Variável temporária em linha (Inline temporary variable). Não seria utilizado a variável por mais do que uma vez, melhor torna-la temporária e sem usar variáveis então.
public void MostraMensagem(string nome, string sobrenome){
    MessageBox.Show("Bom Dia, " + nome + " " + sobrenome);
}

//Programa 4 - (4) Algoritmo de substituição. Ao invés de usar muitos ifs aninhados, é melhor e mais conciso se o resultado deles é o mesmo
// como nesse caso, juntar todos em um if só.
String pessoaEncontrada(String[] pessoa) {
    for (int i = 0; i < pessoa.length; i++) {
        if (pessoa[i].equals("João") || pessoa[i].equals("Maria") || pessoa[i].equals("Pedro")) {
            return pessoa[i];
        }
    }
    return "";
}

// parte 2 dos exercícios:

// EXTRACT METHOD. No caso, extrair a lógica para criar função repetível separada
public class Somacao {
    public static void Somar() {
        somarEImprimir("a","b", 3, 7);
        somarEImprimir("x","y", 1372, 2816);
        somarEImprimir("w","z", 271, 865);
    }

    private static void somarEImprimir(String letra, String letra2, int primeiro, int segundo) {
        int soma = primeiro + segundo;
        System.out.println("Somando " + letra + " e " + letra2);
        System.out.println("Resultado da soma de " + letra + " e " + letra2 + ":" + soma);
    }
}



// EXTRACT METHOD. No caso, extrair a lógica para criar função repetível separada. Mesma coisa de antes.
public class MediaDeVendas {
    private int totalDeVendas;
    private double valorTotalVendido;

    public void calcularMediaDeVendas() {
        imprimirMedia("Agosto", 372, 1726493.00);
        imprimirMedia("Setembro", 472, 1836917.15);
    }

    private void imprimirMedia(String mes, int totalVendas, double valorTotal) {
        System.out.println("Vendas de " + mes);
        this.totalDeVendas = totalVendas;
        this.valorTotalVendido = valorTotal;
        double valorMedioPorVenda = this.valorTotalVendido / this.totalDeVendas;
        System.out.println("Valor Médio por Venda em " + mes + ": " + valorMedioPorVenda);
    }
}
