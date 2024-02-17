/**
 * @file Subject.java
 * @brief Define a interface Subject no contexto do padrão Observer.
 */

/**
 * @interface Subject
 * @brief Interface para um subject no contexto do padrão Observer.
 */
public interface Subject {
    /**
     * @brief Adiciona um observador à lista de observadores.
     * @param observer O observador a ser adicionado.
     */
    void addObserver(Observer observer);

    /**
     * @brief Remove um observador da lista de observadores.
     * @param observer O observador a ser removido.
     */
    void removeObserver(Observer observer);

    /**
     * @brief Notifica todos os observadores sobre um evento relacionado a um aluno sendo adicionado na lista do CadastraAluno.
     * @param aluno O objeto Aluno envolvido no evento.
     */
    void notifyAlunoObservers(Aluno aluno);
    // Poderia adicionar outros observers aqui seguindo a mesma lógica
}
