/**
 * @file CadastroObserver.java
 * @brief Define a classe CadastroObserver, que implementa a interface Observer.
 */

/**
 * @class CadastroObserver
 * @implements Observer
 * @brief Implementa a interface Observer para receber notificações sobre novos alunos cadastrados.
 */
public class CadastroObserver implements Observer {
    private String nome;

    /**
     * @brief Construtor da classe CadastroObserver.
     * @param nome O nome do observador.
     */
    public CadastroObserver(String nome) {
        this.nome = nome;
    }

    /**
     * @brief Atualiza o observador com a notificação de um novo aluno cadastrado.
     * @param aluno O objeto Aluno que foi cadastrado.
     */
    @Override
    public void updateAluno(Aluno aluno) {
        System.out.println(nome + " recebeu a notificação: Novo aluno cadastrado - " + aluno.getNome());
    }
    // Posso adicionar outros updates de outros observers.
}
