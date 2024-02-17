/**
 * @file Observer.java
 * @brief Define a interface Observer no contexto do padrão Observer.
 */

/**
 * @interface Observer
 * @brief Interface para observadores no contexto do padrão Observer.
 */
public interface Observer {
    /**
     * @brief Avisa para os observadores uma mudança na lista do CadastroAluno.
     * @param aluno O objeto Aluno envolvido no evento de atualização da lista do CadastroAluno.
     */
    void updateAluno(Aluno aluno);
    // Poderia adicionar novos observers aqui
}
