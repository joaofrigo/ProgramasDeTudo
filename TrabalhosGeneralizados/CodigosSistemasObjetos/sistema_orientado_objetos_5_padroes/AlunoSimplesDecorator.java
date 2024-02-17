/**
 * @file AlunoSimplesDecorator.java
 * @brief Define a classe AlunoSimplesDecorator, que implementa a interface DetalhesAluno como parte de um decorator.
 */

/**
 * @class AlunoSimplesDecorator
 * @implements DetalhesAluno
 * @brief implementa a interface DetalhesAluno para mostrar detalhes simplificados de um aluno, decorando a exibição padrão.
 * @dot
 * digraph AlunoSimplesDecorator {
 *   node [style="filled" fillcolor="#FF69B4" shape="rectangle"];
 *   AlunoSimplesDecorator [label="AlunoSimplesDecorator"];
 *   DetalhesAluno [label="DetalhesAluno"];
 *   AlunoSimplesDecorator -> DetalhesAluno;
 * }
 * @enddot
 */
public class AlunoSimplesDecorator implements DetalhesAluno {

    /**
     * @brief mostra detalhes simplificados do aluno, decorando a exibição padrão.
     * @param aluno o objeto Aluno para o qual os detalhes serão mostrados.
     */
    @Override
    public void mostrarDetalhes(Aluno aluno) {
        System.out.println("Nome: " + aluno.getNome());
        System.out.println("Matrícula: " + aluno.getMatricula());
        System.out.println("Curso: " + aluno.getCurso());
        System.out.println("----------------------------------------");
    }
}
