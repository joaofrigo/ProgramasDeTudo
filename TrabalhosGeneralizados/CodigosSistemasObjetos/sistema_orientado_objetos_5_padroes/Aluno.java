/**
 * @file aluno.java
 * @brief define a classe aluno que representa um estudante.
 */

/**
 * @class aluno
 * @brief representa um aluno com informações como nome, matrícula, curso, endereço, idade e email de contato.
 *
 * esta classe possui um construtor privado e um padrão de design builder para criar instâncias de aluno com configurações opcionais.
 */
public class Aluno {
    // Atributos da classe
    private String nome;
    private int matricula;
    private String curso;
    private String endereco;
    private int idade;
    private String email_contato;

    // Construtor privado para impedir a criação direta de objetos aluno
    private Aluno() {}

    /**
     * @class builder
     * @brief um padrão de design builder para configurar e construir instâncias de aluno.
     */
    public static class Builder {
        private String nome;
        private int matricula;
        private String endereco;
        private int idade;
        private String curso = ""; // Valor padrão é "" caso não precise do curso ou simplesmente ainda não tenha escolhido
        private String email_contato = ""; // Valor padrão é "" por que as vezes pode não se ter

        /**
         * @brief construtor do builder requerendo os parâmetros obrigatórios.
         * @param nome o nome do aluno.
         * @param matricula o número da matrícula do aluno.
         * @param endereco o endereço do aluno.
         * @param idade a idade do aluno.
         */
        public Builder(String nome, int matricula, String endereco, int idade) {
            this.nome = nome;
            this.matricula = matricula;
            this.endereco = endereco;
            this.idade = idade;
        }

        /**
         * @brief método para configurar o curso do aluno (opcional).
         * @param curso o curso do aluno.
         * @return uma referência para o próprio builder, permitindo chamadas encadeadas.
         */
        public Builder curso(String curso) {
            this.curso = curso;
            return this;
        }

        /**
         * @brief método para configurar o email de contato do aluno (opcional).
         * @param email_contato o email de contato do aluno.
         * @return uma referência para o próprio builder, permitindo chamadas encadeadas.
         */
        public Builder emailContato(String email_contato) {
            this.email_contato = email_contato;
            return this;
        }

        /**
         * @brief método para construir a instância final de aluno.
         * @return uma instância de aluno configurada com os parâmetros fornecidos.
         */
        public Aluno build() {
            Aluno aluno = new Aluno();
            aluno.nome = this.nome;
            aluno.matricula = this.matricula;
            aluno.curso = this.curso;
            aluno.endereco = this.endereco;
            aluno.idade = this.idade;
            aluno.email_contato = this.email_contato;
            return aluno;
        }
    }

    // Métodos getters e setters

    /**
     * @brief Getter para o nome do aluno.
     * @return O nome do aluno.
     */
    public String getNome() {
        return nome;
    }

    /**
     * @brief Setter para o nome do aluno.
     * @param nome O novo nome do aluno.
     */
    public void setNome(String nome) {
        this.nome = nome;
    }

    /**
     * @brief Getter para a matrícula do aluno.
     * @return A matrícula do aluno.
     */
    public int getMatricula() {
        return matricula;
    }

    /**
     * @brief Setter para a matrícula do aluno.
     * @param matricula A nova matrícula do aluno.
     */
    public void setMatricula(int matricula) {
        this.matricula = matricula;
    }

    /**
     * @brief Getter para o curso do aluno.
     * @return O curso do aluno.
     */
    public String getCurso() {
        return curso;
    }

    /**
     * @brief Setter para o curso do aluno.
     * @param curso O novo curso do aluno.
     */
    public void setCurso(String curso) {
        this.curso = curso;
    }

    /**
     * @brief Getter para o endereço do aluno.
     * @return O endereço do aluno.
     */
    public String getEndereco() {
        return endereco;
    }

    /**
     * @brief Setter para o endereço do aluno.
     * @param endereco O novo endereço do aluno.
     */
    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }

    /**
     * @brief Getter para a idade do aluno.
     * @return A idade do aluno.
     */
    public int getIdade() {
        return idade;
    }

    /**
     * @brief Setter para a idade do aluno.
     * @param idade A nova idade do aluno.
     */
    public void setIdade(int idade) {
        this.idade = idade;
    }

    /**
     * @brief Getter para o email de contato do aluno.
     * @return O email de contato do aluno.
     */
    public String getEmail_contato() {
        return email_contato;
    }

    /**
     * @brief Setter para o email de contato do aluno.
     * @param email_contato O novo email de contato do aluno.
     */
    public void setEmail_contato(String email_contato) {
        this.email_contato = email_contato;
    }
}
