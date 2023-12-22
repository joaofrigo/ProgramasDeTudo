
CALL loop_json();

DROP PROCEDURE IF EXISTS loop_json;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json()
BEGIN
	DECLARE json, products, product VARCHAR(5000);
	DECLARE indexador INT;
	DECLARE indexador2 INT DEFAULT 0;
    DECLARE ID INT DEFAULT 0;
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
    -- SELECT json.json->'$.visitors.data' INTO products;
    -- SET indexador = (SELECT COUNT (*) FROM json);
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.visitors.data')) FROM json WHERE indexador = json.id);
        INSERT INTO dashboard_visitors (hits_count, visitors_count) VALUES (indexador, indexador2);
        -- WHILE indexador2
		SELECT indexador - 1 INTO indexador;
	END WHILE;

END $$
DELIMITER ;

-- DROP TABLE dashboard_visitors;