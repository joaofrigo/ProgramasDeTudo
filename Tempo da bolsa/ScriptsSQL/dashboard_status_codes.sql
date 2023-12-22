CREATE TABLE IF NOT EXISTS dashboard_status_codes(
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    json_id INT, FOREIGN KEY (json_id) REFERENCES json (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  longtext
);

SET SESSION wait_timeout = 31536000;

CREATE TABLE IF NOT EXISTS items_status_codes(
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    id_status_codes INT, FOREIGN KEY (id_status_codes) REFERENCES dashboard_status_codes (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  longtext
);

DROP PROCEDURE IF EXISTS loop_json_dashboard_status_codes;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json_dashboard_status_codes()
BEGIN
	DECLARE indexador INT; -- Json atual
	DECLARE indexador2 INT DEFAULT 0; -- indexador do data do json
    DECLARE indexador3 INT DEFAULT 0; -- indexador do items dentro do data
    DECLARE ultimo_id INT; -- o ultimo ID alterado com auto_increment.
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.status_codes.data')) FROM json WHERE indexador = json.id); -- tamanho do data atual
        WHILE indexador2 > 0 DO -- itera sobre o data
			INSERT INTO dashboard_status_codes (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent,
            data, json_id)
            SELECT
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].hits.count')),
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].hits.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].visitors.count')),
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].visitors.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].bytes.count')),
			JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].bytes.percent')),
            JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].data')),
            indexador
            FROM json
            WHERE indexador = json.id; -- pega valores apenas desse data
            -- LIMIT 2; 
            SET indexador3 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items'))) FROM json WHERE indexador = json.id); -- tamanho do items atual
			SET ultimo_id = LAST_INSERT_ID();-- O ultimo ID alterado por AUTO_INCREMENT
            WHILE indexador3 > 0 DO -- itera sobre o Items
				INSERT INTO items_status_codes (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent,
				data, id_status_codes)
				SELECT
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].hits.count')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].hits.percent')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].visitors.count')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].visitors.percent')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].bytes.count')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].bytes.percent')),
				JSON_EXTRACT(json.json, CONCAT('$.status_codes.data[', indexador2 - 1, '].items[', indexador3 - 1, '].data')),
                ultimo_id
				FROM json
				WHERE indexador = json.id; -- pega valores apenas desse data
                -- INSERT INTO items_status_codes (id_status_codes)
                -- SELECT id from dashboard_status_codes
                SELECT indexador3 - 1 into indexador3;
			END WHILE;
            --
			SELECT indexador2 - 1 INTO indexador2;
		END WHILE;
		SELECT indexador - 1 INTO indexador;
	END WHILE;
END $$
DELIMITER ;

CALL loop_json_dashboard_status_codes;