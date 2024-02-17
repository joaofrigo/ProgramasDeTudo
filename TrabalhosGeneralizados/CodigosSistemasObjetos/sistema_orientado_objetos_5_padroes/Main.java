/**
 * @file Main.java
 * @brief Implementação da classe Main para interação com o sistema de cadastro de alunos.
 */

import java.util.Scanner;

/**
 * @class Main
 * @brief Classe principal para interação com o sistema de cadastro de alunos.
 */
public class Main {
    private static Scanner scanner = new Scanner(System.in);

    /**
     * @brief Função principal que permite a interação com o sistema de cadastro de alunos.
     * @param args Argumentos da linha de comando (não utilizados).
     */
    public static void main(String[] args) {
        CadastroAluno cadastro = CadastroAluno.getInstancia();
        Aluno aluno;

        while (true) {
            System.out.println("Escolha uma opção:");
            System.out.println("1. Cadastrar Aluno com estratégia de curso");
            System.out.println("2. Cadastrar Aluno com estratégia de idade");
            System.out.println("3. Cadastrar Aluno com estratégia de matrícula");
            System.out.println("4. Adicionar observer na lista de alunos");
            System.out.println("5. Visualização simples da lista de alunos");
            System.out.println("6. Visualização extendida da lista de alunos");
            System.out.println("0. Sair");

            int escolha = scanner.nextInt();
            scanner.nextLine(); // Consumir a quebra de linha

            switch (escolha) {
                case 1:
                    aluno = cadastro.criarAlunoComInput();
                    cadastro.cadastrarAluno(aluno, "curso");
                    break;
                case 2:
                    aluno = cadastro.criarAlunoComInput();
                    cadastro.cadastrarAluno(aluno, "idade");
                    break;
                case 3:
                    aluno = cadastro.criarAlunoComInput();
                    cadastro.cadastrarAluno(aluno, "matricula");
                    break;
                case 4:
                    System.out.println("Nome do observer?");
                    String nome = scanner.nextLine();
                    CadastroObserver observer = new CadastroObserver(nome);
                    cadastro.addObserver(observer);
                    break;
                case 5:
                    cadastro.setDetalhesAluno(new AlunoSimplesDecorator());
                    cadastro.listarAlunos();
                    break;
                case 6:
                    cadastro.setDetalhesAluno(new AlunoDetalhadoDecorator());
                    cadastro.listarAlunos();
                    break;
                case 0:
                    System.out.println("Encerrando o programa.");
                    scanner.close();
                    return;
                default:
                    System.out.println("Opção inválida. Tente novamente.");
            }
        }
    }
}


// documentação doxygem, diagrama de classes, user stories Diagrama de sequência



    


    
    
    
    
    
    

    

    
    
    
    



        /*
        Aluno aluno1 = new Aluno.Builder("João", 123, "Rua A", 20) // parte obrigatória
                            .emailContato("joao@example.com") // parte opcional
                            .curso("Engenharia") // parte opcional
                            .build();

        Aluno aluno2 = new Aluno.Builder("Maria", 456, "Rua B", 22) // parte obrigatória
                            .emailContato("maria@example.com") // parte opcional
                            .build();

        // Criação de observadores
        CadastroObserver observer1 = new CadastroObserver("Observer1");
        CadastroObserver observer2 = new CadastroObserver("Observer2");

        // Adição de observadores ao CadastroAluno
        CadastroAluno cadastroAluno = CadastroAluno.getInstancia();
        cadastroAluno.addObserver(observer1);
        cadastroAluno.addObserver(observer2);

        // Cadastrando alunos
        cadastroAluno.cadastrarAluno(aluno1, "idade");
        cadastroAluno.cadastrarAluno(aluno2, "curso");
        */
