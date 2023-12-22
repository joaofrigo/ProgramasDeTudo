
DROP PROCEDURE IF EXISTS inserir_colunas;
DROP PROCEDURE IF EXISTS inserir_tables;
DROP PROCEDURE IF EXISTS inserir_procedure;
DROP PROCEDURE IF EXISTS inserir_database;

DELIMITER //

CREATE PROCEDURE inserir_procedure()  -- Verificar se a tabela já existe
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'nome_do_banco_de_dados' -- verifica se database existe  -- ESCREVER CÒDIGO AQUI 
    )
	THEN
		IF NOT EXISTS (
		SELECT 1 
        FROM INFORMATION_SCHEMA.ROUTINE 
        WHERE ROUTINE_NAME  = 'nome_procedure' -- verifica se procedure NÂO existe  -- ESCREVER CÒDIGO AQUI 
        ) 	-- Se não existe essa procedure, adicionar a procedure
        THEN
        -- ESCREVER CÒDIGO AQUI 
        execute IMMEDIATE 'CREATE PROCEDURE nome_procedure';
		-- CREATE PROCEDURE procedure_teste()
        -- BEGIN
        -- END;
        -- PAROU A ESCRITA DE CÓDIGO
        ELSE
        SELECT 'A procedure já existe';
        END IF;
	ELSE
    SELECT 'A database não existe';
        
	END IF;
END //

CREATE PROCEDURE inserir_tables()  -- Verificar se a tabela já existe
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'nome_do_banco_de_dados' -- verifica se database existe  -- ESCREVER CÒDIGO AQUI 
    )
	THEN
		IF NOT EXISTS (
		SELECT 1 
        FROM INFORMATION_SCHEMA.TABLE 
        WHERE TABLE_NAME = 'nome_table' -- verifica se table NÂO existe  -- ESCREVER CÒDIGO AQUI 
        ) 	-- Se não existe essa table, adicionar a table na database
        THEN
        -- ESCREVER CÒDIGO AQUI 
		CREATE TABLE nome_do_banco_de_dados.nome_table (ID INT AUTO_INCREMENT, PRIMARY KEY (ID));
        -- PAROU A ESCRITA DE CÓDIGO
        ELSE
        SELECT 'A table já existe';
        END IF;
	ELSE
    SELECT 'A database não existe';
        
	END IF;
END //

CREATE PROCEDURE inserir_colunas()
BEGIN
    -- Verificar se a tabela já existe
    IF EXISTS (
        SELECT 1 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'nome_do_banco_de_dados' -- verifica se existe  -- ESCREVER CÒDIGO AQUI 
        AND TABLE_NAME = 'nome_table' -- verifica se existe  -- ESCREVER CÒDIGO AQUI 
    )
	THEN
		IF NOT EXISTS (
		SELECT 1 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE COLUMN_NAME = 'coluna_exemplo' -- verifica se NÂO existe  -- ESCREVER CÒDIGO AQUI 
        ) 	-- Se não existe essa coluna, adicionar a nova coluna na tabela
        THEN
        -- ESCREVER CÒDIGO AQUI 
		ALTER TABLE nome_table -- altera a table que tem o mesmo nome da TABLE_NAME
		ADD coluna_exemplo INT default 0;
        -- PAROU A ESCRITA DE CÓDIGO
        ELSE
        SELECT 'a coluna já existe';
        END IF;
	ELSE
    SELECT 'A table ou database não existe';
        
	END IF;
END //

DELIMITER ;

CALL inserir_tables;
CALL inserir_colunas;
CALL inserir_procedure;









/*DROP PROCEDURE inserir_colunas_exemplo;

DELIMITER //

CREATE PROCEDURE inserir_colunas_exemplo()
BEGIN
    -- Verificar se a tabela já existe
    IF NOT EXISTS (
        SELECT 1 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'nome_do_banco_de_dados'
        AND TABLE_NAME = 'exemplo'
        -- AND COLUMN_NAME = 'coluna_exemplo'
    )
	THEN
		-- Adicionar a nova coluna na tabela
		ALTER TABLE exemplo
		ADD coluna_exemplo INT default 0;
	ELSE
    SELECT 'A coluna não existe';
        
	END IF;
END //

DELIMITER ;

CALL inserir_colunas_exemplo;*/

