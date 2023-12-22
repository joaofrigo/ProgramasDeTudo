DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json_dashboard_requests()
BEGIN
	DECLARE indexador INT;
	DECLARE indexador2 INT DEFAULT 0;
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.requests.data')) FROM json WHERE indexador = json.id); -- tamanho do data atual
        WHILE indexador2 > 0 DO -- itera sobre o data
			INSERT INTO dashboard_requests (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent,
            method , protocol, data, json_id)
            SELECT
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].hits.count')),
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].hits.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].visitors.count')),
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].visitors.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].bytes.count')),
			JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].bytes.percent')),
            JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].method')),
            JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].protocol')),
            JSON_EXTRACT(json.json, CONCAT('$.requests.data[', indexador2 - 1, '].data')),
            indexador
            FROM json
            WHERE indexador = json.id; -- pega valores apenas desse data
            -- LIMIT 2;
			SELECT indexador2 - 1 INTO indexador2;
		END WHILE;
		SELECT indexador - 1 INTO indexador;
	END WHILE;
END $$
DELIMITER ;