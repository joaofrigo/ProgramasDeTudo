CREATE TABLE IF NOT EXISTS dashboard_not_found (
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    json_id INT, FOREIGN KEY (json_id) REFERENCES json (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  varchar(2000),
    method varchar(120),
    protocol varchar(120)
) COLLATE utf8mb4_unicode_ci;

DROP PROCEDURE IF EXISTS loop_json_dashboard_not_found;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json_dashboard_not_found()
BEGIN
	DECLARE indexador INT;
	DECLARE indexador2 INT DEFAULT 0;
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.not_found.data')) FROM json WHERE indexador = json.id); -- tamanho do data atual
        WHILE indexador2 > 0 DO -- itera sobre o data
			INSERT INTO dashboard_not_found (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent, 
             data, method, protocol, json_id)
            SELECT
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].hits.count')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].hits.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].visitors.count')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].visitors.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].bytes.count')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].bytes.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].data')),,
			JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].method')),
            JSON_EXTRACT(json.json, CONCAT('$.not_found.data[', indexador2 - 1, '].protocol')),
            indexador
            FROM json
            WHERE indexador = json.id -- pega valores apenas desse data
            LIMIT 2;
			SELECT indexador2 - 1 INTO indexador2;
		END WHILE;
		SELECT indexador - 1 INTO indexador;
	END WHILE;
END $$
DELIMITER ;

CALL loop_json_dashboard_not_found;