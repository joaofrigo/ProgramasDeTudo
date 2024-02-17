/**
 * @file DetalhesAluno.java
 * @brief Define a interface DetalhesAluno no contexto do padrão Decorator.
 */

/**
 * @interface DetalhesAluno
 * @brief Interface para mostrar detalhes de um aluno no contexto do padrão Decorator.
 * @dot
 * digraph DetalhesAluno {
 *   node [style="filled" fillcolor="#FF69B4" shape="rectangle"];
 *   DetalhesAluno [label="DetalhesAluno"];
 * }
 * @enddot
 */
public interface DetalhesAluno {
    /**
     * @brief Mostra os detalhes do aluno.
     * @param aluno O objeto Aluno cujos detalhes serão mostrados.
     */
    void mostrarDetalhes(Aluno aluno);
}
