/**
 * @file AlunoDetalhadoDecorator.java
 * @brief define a classe AlunoDetalhadoDecorator, que implementa a interface DetalhesAluno como parte de um decorator.
 */

/**
 * @class AlunoDetalhadoDecorator
 * @implements DetalhesAluno
 * @brief implementa a interface DetalhesAluno para mostrar detalhes aprimorados de um aluno, decorando a exibição padrão.
 *  * @dot
 * digraph AlunoDetalhadoDecorator {
 *   node [style="filled" fillcolor="#FF69B4" shape="rectangle"];
 *   AlunoDetalhadoDecorator [label="AlunoDetalhadoDecorator"];
 *   DetalhesAluno [label="DetalhesAluno"];
 *   AlunoDetalhadoDecorator -> DetalhesAluno;
 * }
 * @enddot
 */
public class AlunoDetalhadoDecorator implements DetalhesAluno {

    /**
     * @brief mostra detalhes aprimorados do aluno, decorando a exibição padrão.
     * @param aluno o objeto aluno para o qual os detalhes serão mostrados.
     */
    @Override
    public void mostrarDetalhes(Aluno aluno) {
        System.out.println("Nome: " + aluno.getNome());
        System.out.println("Matrícula: " + aluno.getMatricula());
        System.out.println("Curso: " + aluno.getCurso());
        System.out.println("Endereço: " + aluno.getEndereco());
        System.out.println("Idade: " + aluno.getIdade());
        System.out.println("Email de Contato: " + aluno.getEmail_contato());
        System.out.println("----------------------------------------");
    }
}
