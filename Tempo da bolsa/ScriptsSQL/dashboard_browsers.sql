CREATE TABLE IF NOT EXISTS dashboard_browsers (
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
);
-- BROWSER é especial, precisa de mais parafernalha
--
--
--
--
--
--
--
--
--
--
DROP PROCEDURE IF EXISTS loop_json_dashboard_browsers;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json_dashboard_browsers()
BEGIN
	DECLARE indexador INT;
	DECLARE indexador2 INT DEFAULT 0;
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.dashboard_browsers.data')) FROM json WHERE indexador = json.id); -- tamanho do data atual
        WHILE indexador2 > 0 DO -- itera sobre o data
			INSERT INTO dashboard_browsers (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent, 
             data, method, protocol, json_id)
            SELECT
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].hits.count')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].hits.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].visitors.count')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].visitors.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].bytes.count')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].bytes.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].data')),,
			JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].method')),
            JSON_EXTRACT(json.json, CONCAT('$.dashboard_browsers.data[', indexador2 - 1, '].protocol')),
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

CALL loop_json_dashboard_browsers;