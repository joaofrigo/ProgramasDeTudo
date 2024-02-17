-- Criar uma tabela para armazenar os dados
 DROP TABLE IF EXISTS id_padrao_com_primary;
-- TRUNCATE id_padrao;

CREATE TABLE IF NOT EXISTS id_padrao_com_primary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor INT
);

DROP PROCEDURE IF EXISTS popular_tabela;

DELIMITER //
CREATE PROCEDURE popular_tabela()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE novo_valor INT;

    WHILE i <= 1366224 DO
        SET novo_valor = FLOOR(RAND() * 1000);

        INSERT INTO id_padrao_com_primary (valor) VALUES 
            (novo_valor),
            (novo_valor),
            (novo_valor),
            (novo_valor),
            (novo_valor),
            (novo_valor);
        
        SET i = i + 6;
    END WHILE;
END;
DELIMITER ;

-- Chamar o procedimento para popular a tabela
CALL popular_tabela();

select * from id_padrao_com_primary;
SELECT id FROM id_padrao_com_primary ORDER BY id DESC LIMIT 1;

# Temos um total de 1366224 linhas no arquivo grande de movie_ratings
