SELECT id FROM json WHERE id = 1; -- Encontra o ID na tabela. Se ele existe não insere, só modifica, se não existe insere.

-- PARTE DO GENERAL
INSERT INTO dashboard_general (json_id, start_date, end_date, date_time, total_requests, 
        valid_requests, failed_requests,generation_time, unique_visitors, unique_files, excluded_hits, 
        unique_referrers, not_found, unique_static_files, log_size, bandwidth, log_path) 
        VALUES (1, "" ,"", 
        "" ,1, 2, 
        3, 7, 12, 
        4, 8, 11, 
        5, 9, 10, 
        6,""); 

UPDATE dashboard_general SET
json_id = 2,
start_date = "",
end_date = "",
date_time = "",
total_requests = 123,
valid_requests = 1232,
failed_requests = 123,
generation_time = 123,
unique_visitors = 123,
unique_files = 123,
excluded_hits = 123,
unique_referrers = 123,
not_found = 123,
unique_static_files = 123,
log_size = 123,
bandwidth = 123,
log_path = ""
WHERE id = 1;

select * from dashboard_general;

-- PARTE DO REQUESTS
SELECT * FROM dashboard_requests;

INSERT INTO dashboard_requests(json_id, hits_count, hits_percent, visitors_count, visitors_percent,
bytes_count, bytes_percent, data, method, protocol)
VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)