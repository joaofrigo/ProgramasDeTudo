
CREATE TABLE IF NOT EXISTS dashboard_visitors(
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    json_id INT, FOREIGN KEY (json_id) REFERENCES json (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  varchar(30)
);

CALL loop_json_dashboard_visitors();

DROP PROCEDURE IF EXISTS loop_json;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS loop_json_dashboard_visitors()
BEGIN
	DECLARE indexador INT;
	DECLARE indexador2 INT DEFAULT 0;
    SET indexador = (SELECT COUNT(*) FROM json); -- tem o tamanho de toda a tabela json
	WHILE indexador > 0 DO -- ID do JSON
		SET indexador2 = (SELECT JSON_LENGTH(JSON_EXTRACT(json.json, '$.visitors.data')) FROM json WHERE indexador = json.id); -- tamanho do data atual
        WHILE indexador2 > 0 DO -- itera sobre o data
			INSERT INTO dashboard_visitors (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent, 
            data, json_id)
            SELECT
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].hits.count')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].hits.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].visitors.count')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].visitors.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].bytes.count')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].bytes.percent')),
			JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', indexador2 - 1, '].data')),
            indexador
            FROM json
            WHERE indexador = json.id; -- pega valores apenas desse data
			SELECT indexador2 - 1 INTO indexador2;
		END WHILE;
		SELECT indexador - 1 INTO indexador;
	END WHILE;
END $$
DELIMITER ;






-- SET @idx := 0;

/*INSERT INTO dashboard_visitors (hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent, data)
SELECT
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].hits.count')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].hits.percent')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].visitors.count')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].visitors.percent')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].bytes.count')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx, '].bytes.percent')),
    JSON_EXTRACT(json.json, CONCAT('$.visitors.data[', @idx := CASE WHEN @idx >= JSON_LENGTH(JSON_EXTRACT(json.json, '$.visitors.data')) - 1 THEN 0 ELSE @idx + 1 END, '].data'))
FROM
    json
LIMIT 10;*/




/*UPDATE dashboard_general
SET json_id = (SELECT id FROM json WHERE dashboard_general.id = json.id);*/
-- LIMIT 10;






/*INSERT INTO dashboard_visitors (json_id, hits_count, hits_percent, visitors_count, visitors_percent, bytes_count, bytes_percent, data)
SELECT
    json.id AS json_id,
    JSON_EXTRACT(data_array, '$.hits.count') AS hits_count,
    JSON_EXTRACT(data_array, '$.hits.percent') AS hits_percent,
    JSON_EXTRACT(data_array, '$.visitors.count') AS visitors_count,
    JSON_EXTRACT(data_array, '$.visitors.percent') AS visitors_percent,
    JSON_EXTRACT(data_array, '$.bytes.count') AS bytes_count,
    JSON_EXTRACT(data_array, '$.bytes.percent') AS bytes_percent,
    JSON_EXTRACT(data_array, '$.data') AS data
FROM
    json,
    (SELECT JSON_ARRAY_ELEMENT(data, num) AS data_array FROM json, 
	(SELECT @row_number:=@row_number+1 AS num FROM json, (SELECT @row_number:=0) AS t) AS nums) AS jt;*/



/*INSERT INTO dashboard_visitors (json_id, hits_count, hits_percent, visitors_count, visitors_percent, bytes_count,
bytes_percent, data)
SELECT
	json.id AS json_id, -- importante para diferenciar cada linha por isso usar tuplas
	JSON_EXTRACT(json.json, '$.visitors.data[*].hits.count') AS hits_count, 
    JSON_EXTRACT(json.json, '$.visitors.data[*].hits.percent') AS hits_percent, 
	JSON_EXTRACT(json.json, '$.visitors.data[*].visitors.count') AS visitors_count,
    JSON_EXTRACT(json.json, '$.visitors.data[*].visitors.percent') AS visitors_percent,
    JSON_EXTRACT(json.json, '$.visitors.data[*].bytes.count') AS bytes_count,
    JSON_EXTRACT(json.json, '$.visitors.data[*].bytes.percent') AS bytes_percent,
    JSON_EXTRACT(json.json, '$.visitors.data[*].data') AS data
    
FROM json;*/

-- UPDATE dashboard_visitors
-- SET json_id = (SELECT id FROM json WHERE dashboard_visitors.id = json.id);