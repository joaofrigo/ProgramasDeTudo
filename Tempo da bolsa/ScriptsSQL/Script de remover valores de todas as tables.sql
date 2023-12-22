TRUNCATE dashboard_requests;
TRUNCATE dashboard_general;
TRUNCATE dashboard_status_codes;
TRUNCATE items_status_codes;

DROP TABLE items_status_codes;
DROP TABLE dashboard_status_codes;
DELETE FROM json; -- isso vai deletar todos os valores do json
ALTER TABLE json AUTO_INCREMENT = 1