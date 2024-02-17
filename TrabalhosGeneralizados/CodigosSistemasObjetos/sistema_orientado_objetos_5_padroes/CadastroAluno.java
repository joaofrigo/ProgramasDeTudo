/**
 * @file CadastroAluno.java
 * @brief Implementação da classe CadastroAluno, que utiliza os padrões Builder, Decorator e Singleton.
 */

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * @class CadastroAluno
 * @brief Representa o cadastro de alunos com suporte aos padrões Singleton, Decorator com uso também de funções Factory Method e Strategy.
 */
public class CadastroAluno implements Subject {
    // singleton: Mantém uma única instância da classe
    private static CadastroAluno instancia = new CadastroAluno();
    private List<Aluno> alunos = new ArrayList<>();
    private List<Observer> observers = new ArrayList<>();
    private DetalhesAluno detalhesAluno; // a estratégia que usaremos no decorator.

    // construtor privado para garantir a unicidade
    private CadastroAluno() {}

    /**
     * @brief Obtém a instância única do CadastroAluno.
     * @return A instância única do CadastroAluno.
     */
    public static CadastroAluno getInstancia() {
        return instancia;
    }

    /**
     * @brief Cria um novo aluno com base nas informações fornecidas pelo usuário.
     * @return O aluno criado.
     */
    public Aluno criarAlunoComInput() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Digite o nome do aluno:");
        String nome = scanner.nextLine();

        System.out.println("Digite a matrícula do aluno:");
        int matricula = Integer.parseInt(scanner.nextLine());

        System.out.println("Digite o endereço do aluno:");
        String endereco = scanner.nextLine();

        System.out.println("Digite a idade do aluno:");
        int idade = Integer.parseInt(scanner.nextLine());

        System.out.println("Digite o curso do aluno (pressione Enter para pular):");
        String curso = scanner.nextLine();
        if (curso.isEmpty()) {
            curso = ""; // define como "" se o usuário não inserir um valor
        }

        System.out.println("Digite o email de contato do aluno (pressione Enter para pular):");
        String email_contato = scanner.nextLine();
        if (email_contato.isEmpty()) {
            email_contato = ""; // define como "" se o usuário não inserir um valor
        }

        // usa o Builder do Aluno para construir o objeto Aluno
        return new Aluno.Builder(nome, matricula, endereco, idade)
                .curso(curso)
                .emailContato(email_contato)
                .build();
    }

    @Override
    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    @Override
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    /**
     * @brief Notifica todos os observadores sobre o novo aluno cadastrado.
     * @param aluno O aluno recém-cadastrado.
     */
    @Override
    public void notifyAlunoObservers(Aluno aluno) {
        for (Observer observer : observers) {
            observer.updateAluno(aluno);
        }
    }

    /**
     * @brief Cadastra um novo aluno, aplicando estratégias de validação com base no critério fornecido.
     * @param aluno O aluno a ser cadastrado.
     * @param criterioValidacao O critério de validação a ser aplicado. Escolha entre "curso", "idade" e "matricula"
     */
    public void cadastrarAluno(Aluno aluno, String criterioValidacao) {
        // factory method: Obter a fábrica de estratégias com base no critério
        ValidacaoStrategyFactory strategyFactory = obterFactoryPorCriterio(criterioValidacao);

        // factory method: Criar a estratégia de validação específica
        ValidacaoStrategy strategy = strategyFactory.criarValidacaoStrategy();

        // strategy: Executar a estratégia de validação
        ValidacaoCadastroResult resultado = strategy.validar(aluno);

        if (resultado.isValid()) {
            // se a validação permitir o cadastro, adiciona o aluno à lista
            alunos.add(aluno);
            System.out.println("Aluno cadastrado: " + aluno.getNome());
            notifyAlunoObservers(aluno);
        } else {
            // se a validação não permitir, exibe a mensagem de rejeição
            System.out.println(resultado.getMensagem());
        }

        // notifica os observadores sobre o novo aluno cadastrado
    }
    
    // método privado para obter a fábrica de estratégias com base no critério
    private ValidacaoStrategyFactory obterFactoryPorCriterio(String criterio) {
        switch (criterio.toLowerCase()) {
            case "idade":
                return new IdadeValidacaoStrategyFactory();
            case "curso":
                return new CursoValidacaoStrategyFactory();
            case "matricula":
                return new MatriculaValidacaoStrategyFactory();
            default:
                throw new IllegalArgumentException("Criterio de validação desconhecido: " + criterio);
        }
    }

    /**
     * @brief Lista os alunos cadastrados, utilizando a estratégia de detalhes configurada com decorator.
     */
    public void listarAlunos() {
        if (alunos.isEmpty()) {
            System.out.println("Nenhum aluno cadastrado.");
        } else {
            System.out.println("Lista de Alunos:");
            for (Aluno aluno : alunos) {
                detalhesAluno.mostrarDetalhes(aluno);
            }
        }
    }

    /**
     * @brief Obtém uma cópia da lista de alunos cadastrados.
     * @return Uma lista de alunos cadastrados.
     */
    public List<Aluno> getAlunos() {
        return new ArrayList<>(alunos);
    }

    /**
     * @brief Define a estratégia de detalhes a ser utilizada no cadastro.
     * @param detalhesAluno A estratégia de detalhes a ser configurada no decorator.
     */
    public void setDetalhesAluno(DetalhesAluno detalhesAluno) {
        this.detalhesAluno = detalhesAluno;
    }

    /**
     * @brief Busca um aluno cadastrado pelo nome.
     * @param nome O nome do aluno a ser buscado.
     * @return O aluno encontrado ou null se não encontrado.
     */
    public Aluno buscarAlunoPorNome(String nome) {
        for (Aluno aluno : alunos) {
            if (aluno.getNome().equals(nome)) {
                return aluno;
            }
        }
        return null; // retorna NULL caso não encontre
    }

    /**
     * @brief Busca um aluno cadastrado pelo curso.
     * @param curso O curso do aluno a ser buscado.
     * @return O aluno encontrado ou null se não encontrado.
     */
    public Aluno buscarAlunoPorCurso(String curso) {
        for (Aluno aluno : alunos) {
            if (aluno.getCurso().equals(curso)) {
                return aluno;
            }
        }
        return null; // retorna NULL caso não encontre
    }

    /**
     * @brief Busca um aluno cadastrado pelo email de contato.
     * @param email O email de contato do aluno a ser buscado.
     * @return O aluno encontrado ou null se não encontrado.
     */
    public Aluno buscarAlunoPorEmail(String email) {
        for (Aluno aluno : alunos) {
            if (aluno.getEmail_contato().equals(email)) {
                return aluno;
            }
        }
        return null; // retorna NULL caso não encontre
    }

    /**
     * @brief Busca um aluno cadastrado pela matrícula.
     * @param matricula A matrícula do aluno a ser buscada.
     * @return O aluno encontrado ou null se não encontrado.
     */
    public Aluno buscarAlunoPorMatricula(int matricula) {
        for (Aluno aluno : alunos) {
            if (aluno.getMatricula() == matricula) {
                return aluno;
            }
        }
        return null; // retorna NULL caso não encontre
    }
}
