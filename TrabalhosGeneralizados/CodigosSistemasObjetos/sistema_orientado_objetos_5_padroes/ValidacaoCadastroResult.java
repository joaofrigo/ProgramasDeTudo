/**
 * @file ValidacaoCadastroResult.java
 * @brief Representa o resultado de uma validação no contexto do CadastraValidacaoManager.
 */

/**
 * @class ValidacaoCadastroResult
 * @brief Representa o resultado de uma validação no contexto do CadastraValidacaoManager.
 */
public class ValidacaoCadastroResult {
    private boolean isValid;
    private String mensagem;

    /**
     * @brief Construtor que inicializa o resultado de validação com os parâmetros fornecidos.
     * @param isValid Indica se a validação foi bem-sucedida ou não.
     * @param mensagem A mensagem associada ao resultado da validação.
     */
    public ValidacaoCadastroResult(boolean isValid, String mensagem) {
        this.isValid = isValid;
        this.mensagem = mensagem;
    }

    /**
     * @brief Verifica se a validação foi bem-sucedida.
     * @return true se a validação foi bem-sucedida, false caso contrário.
     */
    public boolean isValid() {
        return isValid;
    }

    /**
     * @brief Obtém a mensagem associada ao resultado da validação.
     * @return A mensagem associada ao resultado da validação.
     */
    public String getMensagem() {
        return mensagem;
    }
}
