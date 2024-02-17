/**
 * @file ValidacaoStrategy.java
 * @brief Define a interface ValidacaoStrategy para estratégias de validação no contexto do padrão Strategy.
 */

import java.util.List;

/**
 * @interface ValidacaoStrategy
 * @brief Interface para estratégias de validação no contexto do padrão Strategy.
 */
interface ValidacaoStrategy {
    /**
     * @brief Valida um aluno com base na estratégia específica.
     * @param aluno O objeto Aluno a ser validado.
     * @return O resultado da validação.
     */
    ValidacaoCadastroResult validar(Aluno aluno);
}

/**
 * @class IdadeValidacaoStrategy
 * @implements ValidacaoStrategy
 * @brief Implementação de estratégia de validação de idade no contexto do padrão Strategy.
 */
class IdadeValidacaoStrategy implements ValidacaoStrategy {
    @Override
    public ValidacaoCadastroResult validar(Aluno aluno) {
        if (aluno.getIdade() >= 18) {
            return new ValidacaoCadastroResult(true, aluno.getNome() + " validado com base na estratégia de idade.");
        } else {
            return new ValidacaoCadastroResult(false, "cadastro do aluno " + aluno.getNome() + " rejeitado com base na estratégia de idade.");
        }
    }
}

/**
 * @class CursoValidacaoStrategy
 * @implements ValidacaoStrategy
 * @brief Implementação de estratégia de validação de curso no contexto do padrão Strategy.
 */
class CursoValidacaoStrategy implements ValidacaoStrategy {
    @Override
    public ValidacaoCadastroResult validar(Aluno aluno) {
        if (aluno.getCurso() != null && !aluno.getCurso().isEmpty()) {
            return new ValidacaoCadastroResult(true, aluno.getNome() + " validado com base na estratégia de curso.");
        } else {
            return new ValidacaoCadastroResult(false, "cadastro do aluno " + aluno.getNome() + " rejeitado com base na estratégia de curso.");
        }
    }
}

/**
 * @class MatriculaValidacaoStrategy
 * @implements ValidacaoStrategy
 * @brief Implementação de estratégia de validação de matrícula no contexto do padrão Strategy.
 */
class MatriculaValidacaoStrategy implements ValidacaoStrategy {
    @Override
    public ValidacaoCadastroResult validar(Aluno aluno) {
        List<Aluno> alunos = CadastroAluno.getInstancia().getAlunos();
        int matriculaAtual = aluno.getMatricula();

        for (Aluno alunoExistente : alunos) {
            if (alunoExistente.getMatricula() == matriculaAtual) {
                return new ValidacaoCadastroResult(false, "cadastro do aluno " + aluno.getNome() + " rejeitado. Matrícula já existente.");
            }
        }

        return new ValidacaoCadastroResult(true, aluno.getNome() + " validado com base na estratégia de matrícula.");
    }
}

/**
 * @interface ValidacaoStrategyFactory
 * @brief Interface para criar estratégias de validação no contexto do padrão Factory Method.
 */
interface ValidacaoStrategyFactory {
    /**
     * @brief Cria uma estratégia de validação específica.
     * @return A estratégia de validação criada.
     */
    ValidacaoStrategy criarValidacaoStrategy();
}

/**
 * @class IdadeValidacaoStrategyFactory
 * @implements ValidacaoStrategyFactory
 * @brief Implementação para criar estratégia de validação de idade no contexto do padrão Factory Method.
 */
class IdadeValidacaoStrategyFactory implements ValidacaoStrategyFactory {
    @Override
    public ValidacaoStrategy criarValidacaoStrategy() {
        return new IdadeValidacaoStrategy();
    }
}

/**
 * @class CursoValidacaoStrategyFactory
 * @implements ValidacaoStrategyFactory
 * @brief Implementação para criar estratégia de validação de curso no contexto do padrão Factory Method.
 */
class CursoValidacaoStrategyFactory implements ValidacaoStrategyFactory {
    @Override
    public ValidacaoStrategy criarValidacaoStrategy() {
        return new CursoValidacaoStrategy();
    }
}

/**
 * @class MatriculaValidacaoStrategyFactory
 * @implements ValidacaoStrategyFactory
 * @brief Implementação para criar estratégia de validação de matrícula no contexto do padrão Factory Method.
 */
class MatriculaValidacaoStrategyFactory implements ValidacaoStrategyFactory {
    @Override
    public ValidacaoStrategy criarValidacaoStrategy() {
        return new MatriculaValidacaoStrategy();
    }
}
