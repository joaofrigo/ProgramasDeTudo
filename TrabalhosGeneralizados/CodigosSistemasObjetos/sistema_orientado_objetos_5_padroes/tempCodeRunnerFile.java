/**
 * @file DetalhesAluno.java
 * @brief Define a interface DetalhesAluno no contexto do padrão Decorator.
 */

/**
 * @interface DetalhesAluno
 * @brief Interface para mostrar detalhes de um aluno no contexto do padrão Decorator.
 */
public interface DetalhesAluno {
    /**
     * @brief Mostra os detalhes do aluno.
     * @param aluno O objeto Aluno cujos detalhes serão mostrados.
     */
    void mostrarDetalhes(Aluno aluno);
}
